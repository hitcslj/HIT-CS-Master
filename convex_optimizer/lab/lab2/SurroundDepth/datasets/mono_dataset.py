# Copyright Niantic 2019. Patent Pending. All rights reserved.
#
# This software is licensed under the terms of the Monodepth2 licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.

from __future__ import absolute_import, division, print_function

import os
import random
import numpy as np
import copy
from PIL import Image  # using pillow-simd for increased speed
import time
import cv2

import torch
import torch.utils.data as data
from torchvision import transforms
import pdb


def pil_loader(path):
    # open path as file to avoid ResourceWarning
    # (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')


class MonoDataset(data.Dataset):
    """Superclass for monocular dataloaders

    Args:
        data_path
        filenames
        height
        width
        frame_idxs
        num_scales
        is_train
    """
    def __init__(self,
                 opt,
                 height,
                 width,
                 frame_idxs,
                 num_scales,
                 is_train=False):
        super(MonoDataset, self).__init__()

        self.opt = opt
        self.height = height
        self.width = width
        self.num_scales = num_scales
        self.interp = Image.ANTIALIAS

        self.frame_idxs = frame_idxs

        self.is_train = is_train

        self.loader = pil_loader
        self.to_tensor = transforms.ToTensor()

        # We need to specify augmentations differently in newer versions of torchvision.
        # We first try the newer tuple version; if this fails we fall back to scalars
        try:
            self.brightness = (0.8, 1.2)
            self.contrast = (0.8, 1.2)
            self.saturation = (0.8, 1.2)
            self.hue = (-0.1, 0.1)
            transforms.ColorJitter.get_params(
                self.brightness, self.contrast, self.saturation, self.hue)
        except TypeError:
            self.brightness = 0.2
            self.contrast = 0.2
            self.saturation = 0.2
            self.hue = 0.1

        self.resize = {}
        for i in range(self.num_scales):
            s = 2 ** i
            self.resize[i] = transforms.Resize((self.height // s, self.width // s),
                                               interpolation=self.interp)
        
    def preprocess(self, inputs, color_aug):
        """Resize colour images to the required scales and augment if required

        We create the color_aug object in advance and apply the same augmentation to all
        images in this item. This ensures that all images input to the pose network receive the
        same augmentation.
        """
        for k in list(inputs):
            frame = inputs[k]
            if "color" in k:
                n, im, i = k
                inputs[(n + "_aug", im, -1)] = []

                for i in range(self.num_scales):
                    inputs[(n, im, i)] = []
                    inputs[(n + "_aug", im, i)] = []
                    #print(n, im, i)
                    for index_spatial in range(6):
                        inputs[(n, im, i)].append(self.resize[i](inputs[(n, im, i - 1)][index_spatial]))

        for k in list(inputs):
            f = inputs[k]
            if "color" in k:
                n, im, i = k
                for index_spatial in range(6):
                    aug = color_aug(f[index_spatial])
                    inputs[(n, im, i)][index_spatial] = self.to_tensor(f[index_spatial])
                    inputs[(n + "_aug", im, i)].append(self.to_tensor(aug))
                
                inputs[(n, im, i)] = torch.stack(inputs[(n, im, i)], dim=0)
                inputs[(n + "_aug", im, i)] = torch.stack(inputs[(n + "_aug", im, i)], dim=0)

    def __len__(self):
        return len(self.filenames)
        #return self.num_frames


    def __getitem__(self, index):
        """Returns a single training item from the dataset as a dictionary.

        Values correspond to torch tensors.
        Keys in the dictionary are either strings or tuples:

            ("color", <frame_id>, <scale>)          for raw colour images,
            ("color_aug", <frame_id>, <scale>)      for augmented colour images,
            ("K", scale) or ("inv_K", scale)        for camera intrinsics,
            "stereo_T"                              for camera extrinsics, and
            "depth_gt"                              for ground truth depth maps.

        <frame_id> is either:
            an integer (e.g. 0, -1, or 1) representing the temporal step relative to 'index',
        or
            "s" for the opposite image in the stereo pair.

        <scale> is an integer representing the scale of the image relative to the fullsize image:
            -1      images at native resolution as loaded from disk
            0       images resized to (self.width,      self.height     )
            1       images resized to (self.width // 2, self.height // 2)
            2       images resized to (self.width // 4, self.height // 4)
            3       images resized to (self.width // 8, self.height // 8)
        """
        inputs = {}

        do_color_aug = self.is_train and random.random() > 0.5
        do_flip = self.is_train and (not self.opt.use_sfm_spatial) and (not self.opt.joint_pose) and random.random() > 0.5

        frame_index = self.filenames[index].strip().split()[0]
        self.get_info(inputs, frame_index, do_flip)

        

        # adjusting intrinsics to match each scale in the pyramid
        if not self.is_train:
            self.frame_idxs = [0]

        for scale in range(self.num_scales):
            for frame_id in  self.frame_idxs:
                inputs[("K", frame_id, scale)] = []
                inputs[("inv_K", frame_id, scale)] = []
    
        for index_spatial in range(6):
            for scale in range(self.num_scales):
                for frame_id in  self.frame_idxs:
                    K = inputs[('K_ori', frame_id)][index_spatial].copy()
        
                    K[0, :] *= (self.width // (2 ** scale)) / inputs['width_ori'][index_spatial]
                    K[1, :] *= (self.height // (2 ** scale)) / inputs['height_ori'][index_spatial]
        
                    inv_K = np.linalg.pinv(K)
        
                    inputs[("K", frame_id, scale)].append(torch.from_numpy(K))
                    inputs[("inv_K", frame_id, scale)].append(torch.from_numpy(inv_K))
    
        for scale in range(self.num_scales):
            for frame_id in  self.frame_idxs:
                inputs[("K",frame_id, scale)] = torch.stack(inputs[("K",frame_id, scale)], dim=0)
                inputs[("inv_K",frame_id, scale)] = torch.stack(inputs[("inv_K", frame_id,scale)], dim=0)

        if do_color_aug:
            #color_aug = transforms.ColorJitter.get_params(
            #    self.brightness, self.contrast, self.saturation, self.hue)
            color_aug = transforms.ColorJitter(
                self.brightness, self.contrast, self.saturation, self.hue)
        else:
            color_aug = lambda x: x

        self.preprocess(inputs, color_aug)

        del inputs[("color", 0, -1)]
        if self.is_train:
            for i in self.frame_idxs[1:]:
                del inputs[("color", i, -1)]
                del inputs[("color_aug", i, -1)]
            for i in self.frame_idxs:
                del inputs[('K_ori', i)]
        else:
            del inputs[('K_ori', 0)]
            
        del inputs['width_ori']
        del inputs['height_ori']

        
        if 'depth' in inputs.keys():
            inputs['depth'] = torch.from_numpy(inputs['depth'])

        if self.is_train:
            inputs["pose_spatial"] = torch.from_numpy(inputs["pose_spatial"])
            for i in self.frame_idxs[1:]:
                inputs[("pose_spatial", i)] = torch.from_numpy(inputs[("pose_spatial", i)])
                
            if self.opt.use_sfm_spatial:
                for j in range(len(inputs['match_spatial'])):
                    inputs['match_spatial'][j] = torch.from_numpy(inputs['match_spatial'][j])
            
            if self.opt.use_fix_mask:
                inputs["mask"] = []
                for i in range(6):
                    temp = cv2.resize(inputs["mask_ori"][i], (self.width, self.height))
                    temp = temp[..., 0]
                    temp = (temp == 0).astype(np.float32)
                    inputs["mask"].append(temp)
                inputs["mask"] = np.stack(inputs["mask"], axis=0)
                inputs["mask"] = np.tile(inputs["mask"][:, None], (1, 2, 1, 1))
                inputs["mask"] = torch.from_numpy(inputs["mask"])
                if do_flip:
                    inputs["mask"] = torch.flip(inputs["mask"], [3])
                del inputs["mask_ori"]


        return inputs

    def get_info(self, inputs, index, do_flip):
        raise NotImplementedError

