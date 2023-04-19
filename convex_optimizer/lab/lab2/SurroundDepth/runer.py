# Copyright Niantic 2019. Patent Pending. All rights reserved.
#
# This software is licensed under the terms of the Monodepth2 licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.

from __future__ import absolute_import, division, print_function

import numpy as np
import time

import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
import tqdm
import pdb

import json

from utils import *
from layers import *

import datasets
import networks
from IPython import embed

import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import cv2
from torch.utils.data import DistributedSampler as _DistributedSampler
import pickle


def get_dist_info(return_gpu_per_machine=False):
    if torch.__version__ < '1.0':
        initialized = dist._initialized
    else:
        if dist.is_available():
            initialized = dist.is_initialized()
        else:
            initialized = False
    if initialized:
        rank = dist.get_rank()
        world_size = dist.get_world_size()
    else:
        rank = 0
        world_size = 1

    if return_gpu_per_machine:
        gpu_per_machine = torch.cuda.device_count()
        return rank, world_size, gpu_per_machine

    return rank, world_size

class DistributedSampler(_DistributedSampler):

    def __init__(self, dataset, num_replicas=None, rank=None, shuffle=True):
        super().__init__(dataset, num_replicas=num_replicas, rank=rank)
        self.shuffle = shuffle

    def __iter__(self):
        if self.shuffle:
            g = torch.Generator()
            g.manual_seed(self.epoch)
            indices = torch.randperm(len(self.dataset), generator=g).tolist()
        else:
            indices = torch.arange(len(self.dataset)).tolist()

        indices = indices[self.rank:self.total_size:self.num_replicas]
    
        return iter(indices)

class Runer:
    def __init__(self, options):
        self.opt = options
        self.log_path = os.path.join(self.opt.log_dir, self.opt.model_name)
        os.makedirs(os.path.join(self.log_path, 'eval'), exist_ok=True)
        os.makedirs(os.path.join(self.log_path, 'models'), exist_ok=True)

        # checking height and width are multiples of 32
        assert self.opt.height % 32 == 0, "'height' must be a multiple of 32"
        assert self.opt.width % 32 == 0, "'width' must be a multiple of 32"

        self.models = {}
        self.parameters_to_train = []

        self.local_rank = self.opt.local_rank
        torch.cuda.set_device(self.local_rank)
        dist.init_process_group(backend='nccl')
        self.device = torch.device("cuda", self.local_rank)

        self.num_scales = len(self.opt.scales)
        self.num_input_frames = len(self.opt.frame_ids)
        self.num_pose_frames = 2 if self.opt.pose_model_input == "pairs" else self.num_input_frames

        assert self.opt.frame_ids[0] == 0, "frame_ids must start with 0"

        self.use_pose_net = not (self.opt.use_stereo and self.opt.frame_ids == [0])

        if self.opt.use_stereo:
            self.opt.frame_ids.append("s")

        self.models["encoder"] = networks.ResnetEncoder(
                self.opt.num_layers, self.opt.weights_init == "pretrained")
        self.models["encoder"] = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.models["encoder"])
        self.models["encoder"] = (self.models["encoder"]).to(self.device)
        self.parameters_to_train += list(self.models["encoder"].parameters())

        self.models["depth"] = networks.DepthDecoder(
            self.opt, self.models["encoder"].num_ch_enc, self.opt.scales)
        self.models["depth"] = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.models["depth"])
        self.models["depth"] = (self.models["depth"]).to(self.device)
        self.parameters_to_train += list(self.models["depth"].parameters())

        if self.use_pose_net:
            if self.opt.pose_model_type == "separate_resnet":

                self.models["pose_encoder"] = networks.ResnetEncoder(
                self.opt.num_layers,
                self.opt.weights_init == "pretrained",
                num_input_images=self.num_pose_frames)

                self.models["pose_encoder"] = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.models["pose_encoder"])
                self.models["pose_encoder"] = self.models["pose_encoder"].to(self.device)
                self.parameters_to_train += list(self.models["pose_encoder"].parameters())

                self.models["pose"] = networks.PoseDecoder(
                    self.models["pose_encoder"].num_ch_enc,
                    num_input_features=1,
                    num_frames_to_predict_for=2)

            elif self.opt.pose_model_type == "shared":
                self.models["pose"] = networks.PoseDecoder(
                    self.models["encoder"].num_ch_enc, self.num_pose_frames)

            elif self.opt.pose_model_type == "posecnn":
                self.models["pose"] = networks.PoseCNN(
                    self.num_input_frames if self.opt.pose_model_input == "all" else 2)

            self.models["pose"] = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.models["pose"])
            self.models["pose"] = (self.models["pose"]).to(self.device)
            self.parameters_to_train += list(self.models["pose"].parameters())

        if self.opt.predictive_mask:
            assert self.opt.disable_automasking, \
                "When using predictive_mask, please disable automasking with --disable_automasking"

            # Our implementation of the predictive masking baseline has the the same architecture
            # as our depth decoder. We predict a separate mask for each source frame.
            self.models["predictive_mask"] = networks.DepthDecoder(
                self.models["encoder"].num_ch_enc, self.opt.scales,
                num_output_channels=(len(self.opt.frame_ids) - 1))
            self.models["predictive_mask"] = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.models["predictive_mask"])
            self.models["predictive_mask"] = (self.models["predictive_mask"]).to(self.device)
            self.parameters_to_train += list(self.models["predictive_mask"].parameters())

        

        if self.opt.load_weights_folder is not None:
            self.load_model()

        for key in self.models.keys():
            self.models[key] = DDP(self.models[key], device_ids=[self.local_rank], output_device=self.local_rank, find_unused_parameters=True, broadcast_buffers=False)

        self.model_optimizer = optim.Adam(self.parameters_to_train, self.opt.learning_rate)
        self.model_lr_scheduler = optim.lr_scheduler.StepLR(
        self.model_optimizer, self.opt.scheduler_step_size, 0.1)

        if self.local_rank == 0:
            self.log_print("Training model named: {}".format(self.opt.model_name))

        # data
        datasets_dict = {"ddad": datasets.DDADDataset,
                         "nusc": datasets.NuscDataset}
        self.dataset = datasets_dict[self.opt.dataset]

        self.opt.batch_size = self.opt.batch_size // 6

        train_dataset = self.dataset(self.opt,
            self.opt.height, self.opt.width,
            self.opt.frame_ids, 4, is_train=True)

        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset, shuffle=True)
        self.train_loader = DataLoader(
            train_dataset, self.opt.batch_size, collate_fn=self.my_collate,
            num_workers=self.opt.num_workers, pin_memory=True, drop_last=True, sampler=train_sampler)
        
        self.num_total_steps = len(self.train_loader) * self.opt.num_epochs
        
        val_dataset = self.dataset(self.opt,
                self.opt.height, self.opt.width,
                self.opt.frame_ids, 4, is_train=False)
        rank, world_size = get_dist_info()
        self.world_size = world_size
        val_sampler = DistributedSampler(val_dataset, world_size, rank, shuffle=False)
        self.val_loader = DataLoader(
            val_dataset, self.opt.batch_size, collate_fn=self.my_collate,
            num_workers=4, pin_memory=True, drop_last=False, sampler=val_sampler)
        
        self.val_iter = iter(self.val_loader)
        self.num_val = len(val_dataset)

        self.opt.batch_size = self.opt.batch_size * 6
        self.num_val = self.num_val * 6

        if not self.opt.no_ssim:
            self.ssim = SSIM()
            self.ssim.to(self.device)

        self.backproject_depth = {}
        self.project_3d = {}
        for scale in self.opt.scales:
            h = self.opt.height // (2 ** scale)
            w = self.opt.width // (2 ** scale)

            self.backproject_depth[scale] = BackprojectDepth(self.opt.batch_size, h, w)
            self.backproject_depth[scale].to(self.device)

            self.project_3d[scale] = Project3D(self.opt.batch_size, h, w)
            self.project_3d[scale].to(self.device)

        self.depth_metric_names = [
            "de/abs_rel", "de/sq_rel", "de/rms", "de/log_rms", "da/a1", "da/a2", "da/a3"]

        if self.local_rank == 0:
            self.log_print("There are {:d} training items and {:d} validation items\n".format(
                len(train_dataset), len(val_dataset)))

        self.save_opts()

    def my_collate(self,batch):
        batch_new = {}
        keys_list = list(batch[0].keys())
        special_key_list = ['id', 'match_spatial']

        for key in keys_list: 
            if key not in special_key_list:
                batch_new[key] = [item[key] for item in batch]
                batch_new[key] = torch.cat(batch_new[key], axis=0)
            else:
                batch_new[key] = []
                for item in batch:
                    for value in item[key]:
                        batch_new[key].append(value)

        return batch_new
    
    def set_train(self):
        """Convert all models to training mode
        """
        for m in self.models.values():
            m.train()

    def set_eval(self):
        """Convert all models to testing/evaluation mode
        """
        for m in self.models.values():
            m.eval()

    def train(self):
        """Run the entire training pipeline
        """
        
        self.step = 1
        
        if self.opt.eval_only:
            self.val()
            if self.local_rank == 0:
               self.evaluation()
            exit()
    
        self.epoch = 0
        self.start_time = time.time()
        for self.epoch in range(self.opt.num_epochs):
            self.train_loader.sampler.set_epoch(self.epoch)
            self.run_epoch()

            
            
    def evaluation(self):
        self.log_print("-> Evaluating {}".format(self.step))

        errors = {}
        eval_types = ['scale-ambiguous', 'scale-aware']
        for eval_type in eval_types:
            errors[eval_type] = {}
        
        for i in range(self.world_size):
            while not os.path.exists(os.path.join(self.log_path, 'eval', '{}.pkl'.format(i))):
                time.sleep(1)
            time.sleep(5)
            with open(os.path.join(self.log_path, 'eval', '{}.pkl'.format(i)), 'rb') as f:
                errors_i = pickle.load(f)
                for eval_type in eval_types:
                    for camera_id in errors_i[eval_type].keys():
                        if camera_id not in errors[eval_type].keys():
                            errors[eval_type][camera_id] = []

                        errors[eval_type][camera_id].append(errors_i[eval_type][camera_id])

        
        num_sum = 0
        for eval_type in eval_types:
            for camera_id in errors[eval_type].keys():
                errors[eval_type][camera_id] = np.concatenate(errors[eval_type][camera_id], axis=0)
            
                if eval_type == 'scale-aware':
                    num_sum += errors[eval_type][camera_id].shape[0]
    
                errors[eval_type][camera_id] = errors[eval_type][camera_id].mean(0)

        assert num_sum == self.num_val
        os.system('rm {}/*'.format(os.path.join(self.log_path, 'eval')))

        for eval_type in eval_types:
            self.log_print("{} evaluation:".format(eval_type))
            mean_errors_sum = 0
            for camera_id in errors[eval_type].keys():
                mean_errors_sum += errors[eval_type][camera_id]
            mean_errors_sum /= len(errors[eval_type].keys())
            errors[eval_type]['all'] = mean_errors_sum

            for camera_id in errors[eval_type].keys():
                mean_errors = errors[eval_type][camera_id]
                self.log_print(camera_id)
                self.log_print(("{:>8} | " * 7).format("abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"))
                self.log_print(("&{: 8.3f}  " * 7).format(*mean_errors.tolist()) + "\\\\")
                


    def val(self):
        """Validate the model on a single minibatch
        """
        self.set_eval()
        
        errors = {}
        eval_types = ['scale-ambiguous', 'scale-aware']
        for eval_type in eval_types:
            errors[eval_type] = {}

        self.models["encoder"].eval()
        self.models["depth"].eval()
        ratios_median = []
        with torch.no_grad():
            loader = self.val_loader
            for idx, data in enumerate(loader):
                input_color = data[("color", 0, 0)].cuda()
                gt_depths = data["depth"].cpu().numpy()
                
                camera_ids = data["id"]
                
                
                features = self.models["encoder"](input_color)
                output = self.models["depth"](features)
                

                pred_disps_tensor, pred_depths = disp_to_depth(output[("disp", 0)], self.opt.min_depth, self.opt.max_depth)

                input_color_flip = torch.flip(input_color, [3])
                features_flip = self.models["encoder"](input_color_flip)
                output_flip = self.models["depth"](features_flip)

                pred_disps_flip_tensor, pred_depths_flip = disp_to_depth(output_flip[("disp", 0)], self.opt.min_depth, self.opt.max_depth)
                pred_disps_flip = post_process_inv_depth(pred_disps_tensor, pred_disps_flip_tensor)
                pred_disps = pred_disps_flip.cpu()[:, 0].numpy()

                for i in range(pred_disps.shape[0]):
                    camera_id = camera_ids[i]
                    if camera_id not in list(errors['scale-aware']):
                        errors['scale-aware'][camera_id] = []
                        errors['scale-ambiguous'][camera_id] = []

                    gt_depth = gt_depths[i]
                    gt_height, gt_width = gt_depth.shape[:2]
    
                    pred_disp = pred_disps[i]
                    pred_depth = 1 / pred_disp                   
                    pred_depth = cv2.resize(pred_depth, (gt_width, gt_height))

                    if self.opt.focal:
                        pred_depth = pred_depth * data[("K", 0, 0)][i, 0, 0].item() / self.opt.focal_scale

                    mask = np.logical_and(gt_depth > self.opt.min_depth, gt_depth < self.opt.max_depth)
                    
     
                    pred_depth = pred_depth[mask]
                    gt_depth = gt_depth[mask]
                    
                    
                    ratio_median = np.median(gt_depth) / np.median(pred_depth)
                    ratios_median.append(ratio_median)
                    pred_depth_median = pred_depth.copy()*ratio_median
        
                    pred_depth_median[pred_depth_median < self.opt.min_depth] = self.opt.min_depth
                    pred_depth_median[pred_depth_median > self.opt.max_depth] = self.opt.max_depth
        
                    errors['scale-ambiguous'][camera_id].append(compute_errors(gt_depth, pred_depth_median))
                    
                    
                    
                    pred_depth[pred_depth < self.opt.min_depth] = self.opt.min_depth
                    pred_depth[pred_depth > self.opt.max_depth] = self.opt.max_depth
        
                    errors['scale-aware'][camera_id].append(compute_errors(gt_depth, pred_depth))
    
        for eval_type in eval_types:
            for camera_id in errors[eval_type].keys():
                errors[eval_type][camera_id] = np.array(errors[eval_type][camera_id])


        with open(os.path.join(self.log_path, 'eval', '{}.pkl'.format(self.local_rank)), 'wb') as f:
            pickle.dump(errors, f)
        
        if self.local_rank == 0:
            self.log_print('median: {}'.format(np.array(ratios_median).mean()))
        
        self.set_train()


    def run_epoch(self):
        """Run a single epoch of training and validation
        """

        torch.autograd.set_detect_anomaly(True)
        if self.local_rank == 0:
            print("Training")
        self.set_train()

        for batch_idx, inputs in enumerate(self.train_loader):

            before_op_time = time.time()

            outputs, losses = self.process_batch(inputs)

            self.model_optimizer.zero_grad()
            losses["loss"].backward()
            self.model_optimizer.step()

            duration = time.time() - before_op_time

            # log less frequently after the first 2000 steps to save time & disk space
            early_phase = batch_idx % self.opt.log_frequency == 0 and self.step < 2000
            late_phase = self.step % 2000 == 0

            if early_phase or late_phase:
                self.log_time(batch_idx, duration, losses["loss"].cpu().data)

                if "depth_gt" in inputs:
                    self.compute_depth_losses(inputs, outputs, losses)
            
            
            if self.step % self.opt.eval_frequency == 0  and self.opt.eval_frequency > 0:
                self.save_model()
                self.val()
                if self.local_rank == 0:
                    self.evaluation()
            
            self.step += 1

        self.model_lr_scheduler.step()

        if self.opt.eval_frequency <= 0:
            self.save_model()
            self.val()
            if self.local_rank == 0:
                self.evaluation()

    def to_device(self, inputs):
        special_key_list = ['id']
        
        match_key_list = ['match_spatial']
        
        for key, ipt in inputs.items():
            if key in special_key_list:
                inputs[key] = ipt
            elif key in match_key_list:
                for i in range(len(inputs[key])):
                    inputs[key][i] = inputs[key][i].to(self.device)
            else:
                inputs[key] = ipt.to(self.device) 

    def process_batch(self, inputs):
        """Pass a minibatch through the network and generate images and losses
        """

        self.to_device(inputs)
        if self.opt.pose_model_type == "shared":
            # If we are using a shared encoder for both depth and pose (as advocated
            # in monodepthv1), then all images are fed separately through the depth encoder.
            all_color_aug = torch.cat([inputs[("color_aug", i, 0)] for i in self.opt.frame_ids])
            all_features = self.models["encoder"](all_color_aug)
            all_features = [torch.split(f, self.opt.batch_size) for f in all_features]

            features = {}
            for i, k in enumerate(self.opt.frame_ids):
                features[k] = [f[i] for f in all_features]

            outputs = self.models["depth"](features[0])
        else:
            # Otherwise, we only feed the image with frame_id 0 through the depth encoder
            features = self.models["encoder"](inputs["color_aug", 0, 0])
            outputs = self.models["depth"](features)

        if self.opt.predictive_mask:
            outputs["predictive_mask"] = self.models["predictive_mask"](features)

        if self.use_pose_net:
            outputs.update(self.predict_poses(inputs, features))

        self.generate_images_pred(inputs, outputs)
        losses = self.compute_losses(inputs, outputs)

        return outputs, losses

    def predict_poses(self, inputs, features):
        """Predict poses between input frames for monocular sequences.
        """
        outputs = {}
        
        if self.num_pose_frames == 2:
            # In this setting, we compute the pose to each source frame via a
            # separate forward pass through the pose network.

            # select what features the pose network takes as input
            if self.opt.pose_model_type == "shared":
                pose_feats = {f_i: features[f_i] for f_i in self.opt.frame_ids}
            else:
                pose_feats = {f_i: inputs["color_aug", f_i, 0] for f_i in self.opt.frame_ids}

            for f_i in self.opt.frame_ids[1:]:
                if f_i != "s":
                    # To maintain ordering we always pass frames in temporal order
                    if f_i < 0:
                        pose_inputs = [pose_feats[f_i], pose_feats[0]]
                    else:
                        pose_inputs = [pose_feats[0], pose_feats[f_i]]

                    if self.opt.pose_model_type == "separate_resnet":
                        pose_inputs = [self.models["pose_encoder"](torch.cat(pose_inputs, 1))]


                    elif self.opt.pose_model_type == "posecnn":
                        pose_inputs = torch.cat(pose_inputs, 1)

                    axisangle, translation = self.models["pose"](pose_inputs, joint_pose=self.opt.joint_pose)
                    outputs[("axisangle", 0, f_i)] = axisangle
                    outputs[("translation", 0, f_i)] = translation

                    # Invert the matrix if the frame id is negative
                    if self.opt.joint_pose:
                        trans = transformation_from_parameters(
                            axisangle[:, 0], translation[:, 0], invert=(f_i < 0))
                        trans = trans.unsqueeze(1).repeat(1, 6, 1, 1).reshape(-1, 4, 4)
                        outputs[("cam_T_cam", 0, f_i)] = torch.linalg.inv(inputs["pose_spatial"]) @ trans @ inputs["pose_spatial"]
                    else:
                        outputs[("cam_T_cam", 0, f_i)] = transformation_from_parameters(
                            axisangle[:, 0], translation[:, 0], invert=(f_i < 0))

        else:
            # Here we input all frames to the pose net (and predict all poses) together
            if self.opt.pose_model_type in ["separate_resnet", "posecnn"]:
                pose_inputs = torch.cat(
                    [inputs[("color_aug", i, 0)] for i in self.opt.frame_ids if i != "s"], 1)

                if self.opt.pose_model_type == "separate_resnet":
                    pose_inputs = [self.models["pose_encoder"](pose_inputs)]

            elif self.opt.pose_model_type == "shared":
                pose_inputs = [features[i] for i in self.opt.frame_ids if i != "s"]

            axisangle, translation = self.models["pose"](pose_inputs)

            for i, f_i in enumerate(self.opt.frame_ids[1:]):
                if f_i != "s":
                    outputs[("axisangle", 0, f_i)] = axisangle
                    outputs[("translation", 0, f_i)] = translation
                    outputs[("cam_T_cam", 0, f_i)] = transformation_from_parameters(
                        axisangle[:, i], translation[:, i])

        return outputs


    def generate_images_pred(self, inputs, outputs):
        """Generate the warped (reprojected) color images for a minibatch.
        Generated images are saved into the `outputs` dictionary.
        """
        for scale in self.opt.scales:
            disp = outputs[("disp", scale)]
            if self.opt.v1_multiscale:
                source_scale = scale
            else:
                disp = F.interpolate(
                    disp, [self.opt.height, self.opt.width], mode="bilinear", align_corners=False)
                source_scale = 0

            _, depth = disp_to_depth(disp, self.opt.min_depth, self.opt.max_depth)
            
            if self.opt.focal:
                depth = depth * inputs[("K", 0, 0)][:, 0, 0][:, None, None, None] / self.opt.focal_scale

            outputs[("depth", 0, scale)] = depth

            for i, frame_id in enumerate(self.opt.frame_ids[1:]):

                if frame_id == "s":
                    T = inputs["stereo_T"]
                else:
                    T = outputs[("cam_T_cam", 0, frame_id)]

                
                # from the authors of https://arxiv.org/abs/1712.00175
                if self.opt.pose_model_type == "posecnn":

                    axisangle = outputs[("axisangle", 0, frame_id)]
                    translation = outputs[("translation", 0, frame_id)]

                    inv_depth = 1 / depth
                    mean_inv_depth = inv_depth.mean(3, True).mean(2, True)

                    T = transformation_from_parameters(
                        axisangle[:, 0], translation[:, 0] * mean_inv_depth[:, 0], frame_id < 0)
                

                cam_points = self.backproject_depth[source_scale](
                    depth, inputs[("inv_K", 0, source_scale)])
                pix_coords = self.project_3d[source_scale](
                    cam_points, inputs[("K", frame_id, source_scale)], T)

                outputs[("sample", frame_id, scale)] = pix_coords

                outputs[("color", frame_id, scale)] = F.grid_sample(
                    inputs[("color", frame_id, source_scale)],
                    outputs[("sample", frame_id, scale)],
                    padding_mode="border", align_corners=True)
                

                if not self.opt.disable_automasking:
                    outputs[("color_identity", frame_id, scale)] = \
                        inputs[("color", frame_id, source_scale)]

                if self.opt.spatial:        
                    T = inputs[('pose_spatial', frame_id)]
        
                    cam_points = self.backproject_depth[source_scale](
                        outputs[("depth", 0, scale)], inputs[("inv_K", 0, source_scale)])

                    K_temp = inputs[("K", 0, source_scale)].clone().reshape(-1, 6, 4, 4)
                    if frame_id == 1:
                        K_temp = K_temp[:, [1, 2, 3, 4, 5, 0]]
                        K_temp = K_temp.reshape(-1, 4, 4)
                    elif frame_id == -1:
                        K_temp = K_temp[:, [5, 0, 1, 2, 3, 4]]
                        K_temp = K_temp.reshape(-1, 4, 4)
                    pix_coords = self.project_3d[source_scale](
                        cam_points, K_temp, T)
        
                    outputs[("sample_spatial", frame_id, scale)] = pix_coords
        
                    B, C, H, W = inputs[("color", 0, source_scale)].shape
                    inputs_temp = inputs[("color", 0, source_scale)].reshape(-1, 6, C, H, W)
                    if self.opt.use_fix_mask:
                        inputs_mask = inputs["mask"].clone().reshape(-1, 6, 2, H, W)
                    if frame_id == 1:
                        inputs_temp = inputs_temp[:, [1, 2, 3, 4, 5, 0]]
                        inputs_temp = inputs_temp.reshape(B, C, H, W)
                        if self.opt.use_fix_mask:
                            inputs_mask = inputs_mask[:, [1, 2, 3, 4, 5, 0]]
                            inputs_mask = inputs_mask.reshape(B, 2, H, W)
                    elif frame_id == -1:
                        inputs_temp = inputs_temp[:, [5, 0, 1, 2, 3, 4]]
                        inputs_temp = inputs_temp.reshape(B, C, H, W)
                        if self.opt.use_fix_mask:
                            inputs_mask = inputs_mask[:, [5, 0, 1, 2, 3, 4]]
                            inputs_mask = inputs_mask.reshape(B, 2, H, W)
                        
                    outputs[("color_spatial", frame_id, scale)] = F.grid_sample(
                        inputs_temp,
                        outputs[("sample_spatial", frame_id, scale)],
                        padding_mode="zeros", align_corners=True)

                    if self.opt.use_fix_mask:
                        outputs[("color_spatial_mask", frame_id, scale)] = F.grid_sample(
                            inputs_mask[:, 0:1],
                            outputs[("sample_spatial", frame_id, scale)],
                            padding_mode="zeros", align_corners=True, mode='nearest').detach()
                    else:
                        outputs[("color_spatial_mask", frame_id, scale)] = F.grid_sample(
                            torch.ones(B, 1, H, W).cuda(),
                            outputs[("sample_spatial", frame_id, scale)],
                            padding_mode="zeros", align_corners=True, mode='nearest').detach()

                        
            if self.opt.use_sfm_spatial:
                outputs[("depth_match_spatial", scale)] = []
                inputs[("depth_match_spatial", scale)] = []

                for j in range(len(inputs["match_spatial"])):
                    pix_norm = inputs['match_spatial'][j][:, :2]
                    pix_norm[..., 0] /= self.opt.width_ori
                    pix_norm[..., 1] /= self.opt.height_ori
                    pix_norm = (pix_norm - 0.5)*2
    
                    depth_billi = F.grid_sample(outputs[("depth", 0, scale)][j].unsqueeze(0), pix_norm.unsqueeze(1).unsqueeze(0),padding_mode="border")
                    depth_billi = depth_billi.squeeze()
    
                    compute_depth = inputs['match_spatial'][j][:, 2]
                    compute_angle = inputs['match_spatial'][j][:, 3]
                    distances1 = inputs['match_spatial'][j][:, 4]
                    distances2 = inputs['match_spatial'][j][:, 5]

                    triangulation_mask = (compute_depth > 0).float()*(compute_depth < 200).float()*(compute_angle > 0.01).float()*(distances1 < self.opt.thr_dis).float()*(distances2 < self.opt.thr_dis).float()
    
                    outputs[("depth_match_spatial", scale)].append(depth_billi[triangulation_mask == 1])
                    inputs[("depth_match_spatial", scale)].append(compute_depth[triangulation_mask == 1])

        
        
        
    def compute_reprojection_loss(self, pred, target):
        """Computes reprojection loss between a batch of predicted and target images
        """
        abs_diff = torch.abs(target - pred)
        l1_loss = abs_diff.mean(1, True)

        if self.opt.no_ssim:
            reprojection_loss = l1_loss
        else:
            ssim_loss = self.ssim(pred, target).mean(1, True)
            reprojection_loss = 0.85 * ssim_loss + 0.15 * l1_loss

        return reprojection_loss

        

    def compute_losses(self, inputs, outputs):
        """Compute the reprojection and smoothness losses for a minibatch
        """
        losses = {}
        total_loss = 0

        for scale in self.opt.scales:
            loss = 0
            reprojection_losses = []
            if self.opt.use_fix_mask:
                output_mask = []


            if self.opt.v1_multiscale:
                source_scale = scale
            else:
                source_scale = 0

            disp = outputs[("disp", scale)]
            color = inputs[("color", 0, scale)]
            target = inputs[("color", 0, source_scale)]

            for frame_id in self.opt.frame_ids[1:]:
                pred = outputs[("color", frame_id, scale)]
                reprojection_losses.append(self.compute_reprojection_loss(pred, target))

            reprojection_losses = torch.cat(reprojection_losses, 1)

            if not self.opt.disable_automasking:
                identity_reprojection_losses = []
                for frame_id in self.opt.frame_ids[1:]:
                    pred = inputs[("color", frame_id, source_scale)]
                    identity_reprojection_losses.append(
                        self.compute_reprojection_loss(pred, target))

                identity_reprojection_losses = torch.cat(identity_reprojection_losses, 1)

                if self.opt.avg_reprojection:
                    identity_reprojection_loss = identity_reprojection_losses.mean(1, keepdim=True)
                else:
                    # save both images, and do min all at once below
                    identity_reprojection_loss = identity_reprojection_losses

            elif self.opt.predictive_mask:
                # use the predicted mask
                mask = outputs["predictive_mask"]["disp", scale]
                if not self.opt.v1_multiscale:
                    mask = F.interpolate(
                        mask, [self.opt.height, self.opt.width],
                        mode="bilinear", align_corners=False)

                reprojection_losses *= mask

                # add a loss pushing mask to 1 (using nn.BCELoss for stability)
                weighting_loss = 0.2 * nn.BCELoss()(mask, torch.ones(mask.shape).cuda())
                loss += weighting_loss.mean()

            if self.opt.use_fix_mask:
                reprojection_losses *= inputs["mask"] #* output_mask

            if self.opt.avg_reprojection:
                reprojection_loss = reprojection_losses.mean(1, keepdim=True)
            else:
                reprojection_loss = reprojection_losses

            if not self.opt.disable_automasking:
                # add random numbers to break ties
                identity_reprojection_loss += torch.randn(
                    identity_reprojection_loss.shape).cuda() * 0.00001

                combined = torch.cat((identity_reprojection_loss, reprojection_loss), dim=1)
            else:
                combined = reprojection_loss

            if combined.shape[1] == 1:
                to_optimise = combined
            else:
                to_optimise, idxs = torch.min(combined, dim=1)

            if not self.opt.disable_automasking:
                outputs["identity_selection/{}".format(scale)] = (
                    idxs > identity_reprojection_loss.shape[1] - 1).float()

            loss += to_optimise.mean()

            if self.opt.use_sfm_spatial:
                depth_losses = []
                for j in range(len(inputs["match_spatial"])):
                    depth_loss = torch.abs(outputs[("depth_match_spatial", scale)][j] - inputs[("depth_match_spatial", scale)][j]).mean()
                    depth_losses.append(depth_loss)
                loss += self.opt.match_spatial_weight * torch.stack(depth_losses).mean()


            if self.opt.spatial:
                reprojection_losses_spatial = []
                spatial_mask = []
                target = inputs[("color", 0, source_scale)]

                for frame_id in self.opt.frame_ids[1:]:
                    pred = outputs[("color_spatial", frame_id, scale)]

                    reprojection_losses_spatial.append(outputs[("color_spatial_mask", frame_id, scale)] * self.compute_reprojection_loss(pred, target))
                    
                    
                reprojection_loss_spatial = torch.cat(reprojection_losses_spatial, 1)
                if self.opt.use_fix_mask:
                    reprojection_loss_spatial *= inputs["mask"]
                
                loss += self.opt.spatial_weight * reprojection_loss_spatial.mean()


            

            mean_disp = disp.mean(2, True).mean(3, True)
            norm_disp = disp / (mean_disp + 1e-7)
            smooth_loss = get_smooth_loss(norm_disp, color)

            loss += self.opt.disparity_smoothness * smooth_loss / (2 ** scale)
            total_loss += loss
            losses["loss/{}".format(scale)] = loss

        total_loss /= self.num_scales
        losses["loss"] = total_loss
        return losses

    def compute_depth_losses(self, inputs, outputs, losses):
        """Compute depth metrics, to allow monitoring during training

        This isn't particularly accurate as it averages over the entire batch,
        so is only used to give an indication of validation performance
        """
        depth_pred = outputs[("depth", 0, 0)]
        depth_pred = torch.clamp(F.interpolate(
            depth_pred, [375, 1242], mode="bilinear", align_corners=False), 1e-3, 80)
        depth_pred = depth_pred.detach()

        depth_gt = inputs["depth_gt"]
        mask = depth_gt > 0

        # garg/eigen crop
        crop_mask = torch.zeros_like(mask)
        crop_mask[:, :, 153:371, 44:1197] = 1
        mask = mask * crop_mask

        depth_gt = depth_gt[mask]
        depth_pred = depth_pred[mask]
        depth_pred *= torch.median(depth_gt) / torch.median(depth_pred)

        depth_pred = torch.clamp(depth_pred, min=1e-3, max=80)

        depth_errors = compute_depth_errors(depth_gt, depth_pred)

        for i, metric in enumerate(self.depth_metric_names):
            losses[metric] = np.array(depth_errors[i].cpu())

    def log_time(self, batch_idx, duration, loss):
        """Print a logging statement to the terminal
        """
        if self.local_rank == 0:
            samples_per_sec = self.opt.batch_size / duration
            time_sofar = time.time() - self.start_time
            training_time_left = (
                self.num_total_steps / self.step - 1.0) * time_sofar if self.step > 0 else 0
            print_string = "epoch {:>3} | batch {:>6} | examples/s: {:5.1f}" + \
                " | loss: {:.5f} | time elapsed: {} | time left: {}"
            
            self.log_print(print_string.format(self.epoch, batch_idx, samples_per_sec, loss,
                                      sec_to_hm_str(time_sofar), sec_to_hm_str(training_time_left)))
            
    
    def log(self, mode, inputs, outputs, losses):
        """Write an event to the tensorboard events file
        """
        writer = self.writers[mode]
        for l, v in losses.items():
            writer.add_scalar("{}".format(l), v, self.step)

        for j in range(min(4, self.opt.batch_size)):  # write a maxmimum of four images
            for s in self.opt.scales:
                for frame_id in self.opt.frame_ids:
                    writer.add_image(
                        "color_{}_{}/{}".format(frame_id, s, j),
                        inputs[("color", frame_id, s)][j].data, self.step)
                    if s == 0 and frame_id != 0:
                        writer.add_image(
                            "color_pred_{}_{}/{}".format(frame_id, s, j),
                            outputs[("color", frame_id, s)][j].data, self.step)

                writer.add_image(
                    "disp_{}/{}".format(s, j),
                    normalize_image(outputs[("disp", s)][j]), self.step)

                if self.opt.predictive_mask:
                    for f_idx, frame_id in enumerate(self.opt.frame_ids[1:]):
                        writer.add_image(
                            "predictive_mask_{}_{}/{}".format(frame_id, s, j),
                            outputs["predictive_mask"][("disp", s)][j, f_idx][None, ...],
                            self.step)

                elif not self.opt.disable_automasking:
                    writer.add_image(
                        "automask_{}/{}".format(s, j),
                        outputs["identity_selection/{}".format(s)][j][None, ...], self.step)

    def save_opts(self):
        """Save options to disk so we know what we ran this experiment with
        """
        models_dir = os.path.join(self.log_path, "models")
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        os.makedirs(os.path.join(self.log_path, "eval"), exist_ok=True)
        to_save = self.opt.__dict__.copy()

        with open(os.path.join(models_dir, 'opt.json'), 'w') as f:
            json.dump(to_save, f, indent=2)

    def save_model(self):
        """Save model weights to disk
        """
        if self.local_rank == 0:
            save_folder = os.path.join(self.log_path, "models", "weights_{}".format(self.step))
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
    
            for model_name, model in self.models.items():
                save_path = os.path.join(save_folder, "{}.pth".format(model_name))
                to_save = model.module.state_dict()
                if model_name == 'encoder':
                    # save the sizes - these are needed at prediction time
                    to_save['height'] = self.opt.height
                    to_save['width'] = self.opt.width
                    to_save['use_stereo'] = self.opt.use_stereo
                torch.save(to_save, save_path)
    
            save_path = os.path.join(save_folder, "{}.pth".format("adam"))
            torch.save(self.model_optimizer.state_dict(), save_path)

    def load_model(self):
        """Load model(s) from disk
        """
        self.opt.load_weights_folder = os.path.expanduser(self.opt.load_weights_folder)

        if self.local_rank == 0:
            assert os.path.isdir(self.opt.load_weights_folder), \
                "Cannot find folder {}".format(self.opt.load_weights_folder)
            self.log_print("loading model from folder {}".format(self.opt.load_weights_folder))

        for n in self.opt.models_to_load:
            if self.local_rank == 0:
                self.log_print("Loading {} weights...".format(n))
            path = os.path.join(self.opt.load_weights_folder, "{}.pth".format(n))
            model_dict = self.models[n].state_dict()
            pretrained_dict = torch.load(path, map_location=torch.device('cpu'))
            pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
            model_dict.update(pretrained_dict)
            self.models[n].load_state_dict(model_dict)

    def load_optimizer(self):
        # loading adam state
        optimizer_load_path = os.path.join(self.opt.load_weights_folder, "adam.pth")
        if os.path.isfile(optimizer_load_path):
            if self.local_rank == 0:
                self.log_print("Loading Adam weights")
            optimizer_dict = torch.load(optimizer_load_path)
            self.model_optimizer.load_state_dict(optimizer_dict)
        else:
            self.log_print("Cannot find Adam weights so Adam is randomly initialized")


    def log_print(self, str):
        print(str)
        with open(os.path.join(self.log_path, 'log.txt'), 'a') as f:
            f.writelines(str + '\n')
