# Copyright Niantic 2019. Patent Pending. All rights reserved.
#
# This software is licensed under the terms of the Monodepth2 licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.

from __future__ import absolute_import, division, print_function

import os
import skimage.transform
import numpy as np
import PIL.Image as pil
import pickle
import pdb
import cv2

from .mono_dataset import MonoDataset


class DDADDataset(MonoDataset):
    """Superclass for different types of KITTI dataset loaders
    """
    def __init__(self, *args, **kwargs):
        super(DDADDataset, self).__init__(*args, **kwargs)

        self.split = 'train' if self.is_train else 'val'
        self.rgb_path = 'data/ddad/raw_data'
        self.depth_path = 'data/ddad/depth'
        self.match_path = 'data/ddad/match'
        self.mask_path = 'data/ddad/mask'

        with open('datasets/ddad/{}.txt'.format(self.split), 'r') as f:
            self.filenames = f.readlines()

        with open('datasets/ddad/info_{}.pkl'.format(self.split), 'rb') as f:
            self.info = pickle.load(f)

        self.camera_ids = ['front', 'front_left', 'back_left', 'back', 'back_right', 'front_right']
        self.camera_names = ['CAMERA_01', 'CAMERA_05', 'CAMERA_07', 'CAMERA_09', 'CAMERA_08','CAMERA_06']
        
    
    def get_info(self, inputs, index_temporal, do_flip):
        inputs[("color", 0, -1)] = []
        if self.is_train:
            if self.opt.use_sfm_spatial:
                inputs["match_spatial"] = []

            for idx, i in enumerate(self.frame_idxs[1:]):
                inputs[("color", i, -1)] = []
                inputs[("pose_spatial", i)] = []

            for idx, i in enumerate(self.frame_idxs):
                inputs[('K_ori', i)] = [] 
            
            inputs['mask_ori'] = []
            inputs["pose_spatial"] = []
        else:
            inputs[('K_ori', 0)] = [] 
            inputs['depth'] = []


        inputs['width_ori'], inputs['height_ori'], inputs['id'] = [], [], []

        scene_id = self.info[index_temporal]['scene_name']

        for index_spatial in range(6):
            inputs['id'].append(self.camera_ids[index_spatial])
            color = self.loader(os.path.join(self.rgb_path, scene_id, 'rgb', 
                                self.camera_names[index_spatial], index_temporal + '.png'))
            inputs['width_ori'].append(color.size[0])
            inputs['height_ori'].append(color.size[1])
            
        
            if not self.is_train:
                depth = np.load(os.path.join(self.depth_path, scene_id, 'depth',
                            self.camera_names[index_spatial], index_temporal + '.npy'))
                inputs['depth'].append(depth.astype(np.float32))
            
            if do_flip:
                color = color.transpose(pil.FLIP_LEFT_RIGHT)
            inputs[("color", 0, -1)].append(color)

            if self.is_train:

                pose_0_spatial = self.info[index_temporal][self.camera_names[index_spatial]]['extrinsics']['quat'].transformation_matrix
                pose_0_spatial[:3, 3] = self.info[index_temporal][self.camera_names[index_spatial]]['extrinsics']['tvec']
            
                inputs["pose_spatial"].append(pose_0_spatial.astype(np.float32))
    
    
            K = np.eye(4).astype(np.float32)
            K[:3, :3] = self.info[index_temporal][self.camera_names[index_spatial]]['intrinsics']
            inputs[('K_ori', 0)].append(K)

            if self.is_train:
                mask = cv2.imread(os.path.join(self.mask_path, self.camera_names[index_spatial], scene_id, 'mask.png'))
                inputs["mask_ori"].append(mask)

                if self.opt.use_sfm_spatial:
                    pkl_path = os.path.join(self.match_path, scene_id, 'match',
                            self.camera_names[index_spatial], index_temporal + '.pkl')
                    with open(pkl_path, 'rb') as f:
                        match_spatial_pkl = pickle.load(f)
                    inputs['match_spatial'].append(match_spatial_pkl['result'].astype(np.float32))

                for idx, i in enumerate(self.frame_idxs[1:]):
                    index_temporal_i = self.info[index_temporal]['context'][idx]

                    K = np.eye(4).astype(np.float32)
                    K[:3, :3] = self.info[index_temporal_i][self.camera_names[index_spatial]]['intrinsics']
                    inputs[('K_ori', i)].append(K)

                    color = self.loader(os.path.join(self.rgb_path, scene_id, 'rgb', 
                                    self.camera_names[index_spatial], index_temporal_i + '.png'))
                    
                    if do_flip:
                        color = color.transpose(pil.FLIP_LEFT_RIGHT)
        
                    inputs[("color", i, -1)].append(color)

                    pose_i_spatial = self.info[index_temporal][self.camera_names[(index_spatial+i)%6]]['extrinsics']['quat'].transformation_matrix
                    pose_i_spatial[:3, 3] = self.info[index_temporal][self.camera_names[(index_spatial+i)%6]]['extrinsics']['tvec']
                    gt_pose_spatial = np.linalg.inv(pose_i_spatial) @ pose_0_spatial
                    inputs[("pose_spatial", i)].append(gt_pose_spatial.astype(np.float32))


    
        if self.is_train:
            for idx, i in enumerate(self.frame_idxs):
                inputs[('K_ori', i)] = np.stack(inputs[('K_ori', i)], axis=0) 
                if i != 0:
                    inputs[("pose_spatial", i)] = np.stack(inputs[("pose_spatial", i)], axis=0)


            inputs['mask_ori'] = np.stack(inputs['mask_ori'], axis=0)   
            inputs['pose_spatial'] = np.stack(inputs['pose_spatial'], axis=0)   
        else:
            inputs[('K_ori', 0)] = np.stack(inputs[('K_ori', 0)], axis=0) 
            inputs['depth'] = np.stack(inputs['depth'], axis=0)   

        for key in ['width_ori', 'height_ori']:
            inputs[key] = np.stack(inputs[key], axis=0)   








