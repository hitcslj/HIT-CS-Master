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
import sys
sys.path.append('/home/linqing.zhao/dgp')
#from dgp.datasets import SynchronizedSceneDataset
import pickle
import pdb
import cv2

from .mono_dataset import MonoDataset

from nuscenes.nuscenes import NuScenes
from pyquaternion import Quaternion

class NuscDataset(MonoDataset):
    """Superclass for different types of KITTI dataset loaders
    """
    def __init__(self, *args, **kwargs):
        super(NuscDataset, self).__init__(*args, **kwargs)

        self.split = 'train' if self.is_train else 'val'
        self.data_path = 'data/nuscenes/raw_data'
        version = 'v1.0-trainval'
        self.nusc = NuScenes(version=version,
                            dataroot=self.data_path, verbose=False)

        self.depth_path = 'data/nuscenes/depth'
        self.match_path = 'data/nuscenes/match'



        with open('datasets/nusc/{}.txt'.format(self.split), 'r') as f:
            self.filenames = f.readlines()

        self.camera_ids = ['front', 'front_left', 'back_left', 'back', 'back_right', 'front_right']
        self.camera_names = ['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT', 'CAM_FRONT_RIGHT']

    
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
            
            inputs["pose_spatial"] = []
        else:
            inputs[('K_ori', 0)] = [] 
            inputs['depth'] = []


        inputs['width_ori'], inputs['height_ori'], inputs['id'] = [], [], []

        rec = self.nusc.get('sample', index_temporal)

        for index_spatial in range(6):
            cam_sample = self.nusc.get(
                'sample_data', rec['data'][self.camera_names[index_spatial]])
            inputs['id'].append(self.camera_ids[index_spatial])
            color = self.loader(os.path.join(self.data_path, cam_sample['filename']))
            inputs['width_ori'].append(color.size[0])
            inputs['height_ori'].append(color.size[1])
            
            if not self.is_train:
                depth = np.load(os.path.join(self.depth_path, cam_sample['filename'][:-4] + '.npy'))
                inputs['depth'].append(depth.astype(np.float32))
            
            if do_flip:
                color = color.transpose(pil.FLIP_LEFT_RIGHT)
            inputs[("color", 0, -1)].append(color)

            ego_spatial = self.nusc.get(
                    'calibrated_sensor', cam_sample['calibrated_sensor_token'])

            if self.is_train:
                pose_0_spatial = Quaternion(ego_spatial['rotation']).transformation_matrix
                pose_0_spatial[:3, 3] = np.array(ego_spatial['translation'])
            
                inputs["pose_spatial"].append(pose_0_spatial.astype(np.float32))
    
            K = np.eye(4).astype(np.float32)
            K[:3, :3] = ego_spatial['camera_intrinsic']
            inputs[('K_ori', 0)].append(K)
            if self.is_train:

                if self.opt.use_sfm_spatial:
                    pkl_path = os.path.join(os.path.join(self.match_path, cam_sample['filename'][:-4] + '.pkl'))
                    with open(pkl_path, 'rb') as f:
                        match_spatial_pkl = pickle.load(f)
                    inputs['match_spatial'].append(match_spatial_pkl['result'].astype(np.float32))

                for idx, i in enumerate(self.frame_idxs[1:]):
                    if i == -1:
                        index_temporal_i = cam_sample['prev']
                    elif i == 1:
                        index_temporal_i = cam_sample['next']
                    cam_sample_i = self.nusc.get(
                        'sample_data', index_temporal_i)
                    ego_spatial_i = self.nusc.get(
                        'calibrated_sensor', cam_sample_i['calibrated_sensor_token'])

                    K = np.eye(4).astype(np.float32)
                    K[:3, :3] = ego_spatial_i['camera_intrinsic']
                    inputs[('K_ori', i)].append(K)

                    color = self.loader(os.path.join(self.data_path, cam_sample_i['filename']))
                    
                    if do_flip:
                        color = color.transpose(pil.FLIP_LEFT_RIGHT)
        
                    inputs[("color", i, -1)].append(color)

                    pose_i_spatial = Quaternion(ego_spatial_i['rotation']).transformation_matrix
                    pose_i_spatial[:3, 3] = np.array(ego_spatial_i['translation'])

    
        if self.is_train:
            for index_spatial in range(6):
                for idx, i in enumerate(self.frame_idxs[1:]):
                    pose_0_spatial = inputs["pose_spatial"][index_spatial]
                    pose_i_spatial = inputs["pose_spatial"][(index_spatial+i)%6]

                    gt_pose_spatial = np.linalg.inv(pose_i_spatial) @ pose_0_spatial
                    inputs[("pose_spatial", i)].append(gt_pose_spatial.astype(np.float32))

            for idx, i in enumerate(self.frame_idxs):
                inputs[('K_ori', i)] = np.stack(inputs[('K_ori', i)], axis=0) 
                if i != 0:
                    inputs[("pose_spatial", i)] = np.stack(inputs[("pose_spatial", i)], axis=0)


            inputs['pose_spatial'] = np.stack(inputs['pose_spatial'], axis=0)   
        else:
            inputs[('K_ori', 0)] = np.stack(inputs[('K_ori', 0)], axis=0) 
            inputs['depth'] = np.stack(inputs['depth'], axis=0)   

        for key in ['width_ori', 'height_ori']:
            inputs[key] = np.stack(inputs[key], axis=0)   








