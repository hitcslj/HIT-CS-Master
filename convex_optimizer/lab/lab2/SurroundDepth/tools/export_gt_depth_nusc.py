import os
import sys
from py import process
import torch
import numpy as np

from PIL import Image
from nuscenes.nuscenes import NuScenes
from pyquaternion import Quaternion

import pdb
import imageio
import concurrent.futures as futures
from scipy.interpolate import griddata
import pickle




class DepthGenerator(object):
    def __init__(self):
        self.data_path = '../data/nuscenes/raw_data'
        version = 'v1.0-trainval'
        self.nusc = NuScenes(version=version,
                            dataroot=self.data_path, verbose=False)

        with open('../datasets/nusc/{}.txt'.format(sys.argv[1]), 'r') as f:
            self.data = f.readlines()

        self.save_path = '../data/nuscenes/depth'
        self.camera_names = ['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT', 'CAM_FRONT_RIGHT']

        for camera_name in self.camera_names:
            os.makedirs(os.path.join(self.save_path, 'samples', camera_name), exist_ok=True)

    def __call__(self, num_workers=8):
        print('generating nuscene depth maps from LiDAR projections')

        def process_one_sample(index):
            index_t = self.data[index].strip()
            rec = self.nusc.get(
                'sample', index_t)

            lidar_sample = self.nusc.get(
                'sample_data', rec['data']['LIDAR_TOP'])
            lidar_pose = self.nusc.get(
                'ego_pose', lidar_sample['ego_pose_token'])
            #yaw = Quaternion(lidar_pose['rotation']).yaw_pitch_roll[0]
            #lidar_rotation = Quaternion(scalar=np.cos(
            #    yaw / 2), vector=[0, 0, np.sin(yaw / 2)])
            lidar_rotation= Quaternion(lidar_pose['rotation'])
            lidar_translation = np.array(lidar_pose['translation'])[:, None]
            lidar_to_world = np.vstack([
                np.hstack((lidar_rotation.rotation_matrix, lidar_translation)),
                np.array([0, 0, 0, 1])
            ])

            # get lidar points
            lidar_file = os.path.join(
                self.data_path, lidar_sample['filename'])
            lidar_points = np.fromfile(lidar_file, dtype=np.float32)
            # lidar data is stored as (x, y, z, intensity, ring index).
            lidar_points = lidar_points.reshape(-1, 5)[:, :4]

            # lidar points ==> ego frame
            sensor_sample = self.nusc.get(
                'calibrated_sensor', lidar_sample['calibrated_sensor_token'])
            lidar_to_ego_lidar_rot = Quaternion(
                sensor_sample['rotation']).rotation_matrix
            lidar_to_ego_lidar_trans = np.array(
                sensor_sample['translation']).reshape(1, 3)

            ego_lidar_points = np.dot(
                lidar_points[:, :3], lidar_to_ego_lidar_rot.T)
            ego_lidar_points += lidar_to_ego_lidar_trans

            homo_ego_lidar_points = np.concatenate(
                (ego_lidar_points, np.ones((ego_lidar_points.shape[0], 1))), axis=1)

            homo_ego_lidar_points = torch.from_numpy(
                homo_ego_lidar_points).float()

            for cam in self.camera_names:
                camera_sample = self.nusc.get(
                    'sample_data', rec['data'][cam])

                car_egopose = self.nusc.get(
                    'ego_pose', camera_sample['ego_pose_token'])
                egopose_rotation = Quaternion(car_egopose['rotation']).inverse
                egopose_translation = - \
                    np.array(car_egopose['translation'])[:, None]
                world_to_car_egopose = np.vstack([
                    np.hstack((egopose_rotation.rotation_matrix,
                               egopose_rotation.rotation_matrix @ egopose_translation)),
                    np.array([0, 0, 0, 1])
                ])

                # From egopose to sensor
                sensor_sample = self.nusc.get(
                    'calibrated_sensor', camera_sample['calibrated_sensor_token'])
                intrinsic = torch.Tensor(sensor_sample['camera_intrinsic'])
                sensor_rotation = Quaternion(sensor_sample['rotation'])
                sensor_translation = np.array(
                    sensor_sample['translation'])[:, None]
                car_egopose_to_sensor = np.vstack([
                    np.hstack(
                        (sensor_rotation.rotation_matrix, sensor_translation)),
                    np.array([0, 0, 0, 1])
                ])
                car_egopose_to_sensor = np.linalg.inv(car_egopose_to_sensor)

                # Combine all the transformation.
                # From sensor to lidar.
                lidar_to_sensor = car_egopose_to_sensor @ world_to_car_egopose @ lidar_to_world
                lidar_to_sensor = torch.from_numpy(lidar_to_sensor).float()

                # load image for debugging
                image_filename = os.path.join(
                    self.data_path, camera_sample['filename'])
                img = Image.open(image_filename)
                img = np.array(img)

                sparse_depth = torch.zeros((img.shape[:2]))

                # Ego(lidar) ==> Camera
                camera_points = torch.mm(
                    homo_ego_lidar_points, lidar_to_sensor.t())
                # depth > 0
                depth_mask = camera_points[:, 2] > 0
                camera_points = camera_points[depth_mask]
                # Camera ==> Pixel
                viewpad = torch.eye(4)
                viewpad[: intrinsic.shape[0], : intrinsic.shape[1]] = intrinsic
                pixel_points = torch.mm(camera_points, viewpad.t())[:, :3]
                pixel_points[:, :2] = pixel_points[:, :2] / \
                    pixel_points[:, 2:3]

                pixel_uv = pixel_points[:, :2].round().long()
                height, width = sparse_depth.shape
                valid_mask = (pixel_uv[:, 0] >= 0) & (
                    pixel_uv[:, 0] <= width - 1) & (pixel_uv[:, 1] >= 0) & (pixel_uv[:, 1] <= height - 1)

                valid_pixel_uv = pixel_uv[valid_mask]
                valid_depth = camera_points[..., 2][valid_mask]

                sparse_depth[valid_pixel_uv[:, 1], valid_pixel_uv[:, 0]
                             ] = valid_depth
                sparse_depth = sparse_depth.numpy()

                np.save(os.path.join(self.save_path, camera_sample['filename'][:-4] + '.npy'), sparse_depth)

            print('finish processing index = {:06d}'.format(index))

        sample_id_list = list(range(len(self.data)))
        with futures.ThreadPoolExecutor(num_workers) as executor:
            executor.map(process_one_sample, sample_id_list)


if __name__ == "__main__":
    model = DepthGenerator()
    model()
