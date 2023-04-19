from __future__ import absolute_import, division, print_function

import os
import sys
import glob
import argparse
import numpy as np
import PIL.Image as pil
from PIL import Image
import matplotlib as mpl
import matplotlib.cm as cm

import pdb
import cv2 as cv
import copy
import scipy.io as sio
import pickle
import joblib
import copyreg
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import multiprocessing
import random

from nuscenes.nuscenes import NuScenes
from pyquaternion import Quaternion



WIDTH=1600
HEIGHT=900

def _pickle_keypoints(point):
    return cv.KeyPoint, (*point.pt, point.size, point.angle,
                         point.response, point.octave, point.class_id)
copyreg.pickle(cv.KeyPoint().__class__, _pickle_keypoints)

def compute_match(src_sift, tgt_sift, src_K, tgt_K, src_auto_mask, tgt_auto_mask, T_gt):
    kp1_ori, des1_ori = src_sift['kp'], src_sift['des']
    kp2_ori, des2_ori = tgt_sift['kp'], tgt_sift['des']

    if des1_ori is None or des2_ori is None:
        return True, 0, 0


    kp1_np = np.array([list(kp1_ori[idx].pt) for idx in range(0, len(kp1_ori))])
    kp2_np = np.array([list(kp2_ori[idx].pt) for idx in range(0, len(kp2_ori))])
    
    mask1 = (kp1_np[:, 0] > 0) *  (kp1_np[:, 0] < WIDTH) * (kp1_np[:, 1] > 0) * (kp1_np[:, 1] < HEIGHT)
    mask2 = (kp2_np[:, 0] > 0) *  (kp2_np[:, 0] < WIDTH) * (kp2_np[:, 1] > 0) * (kp2_np[:, 1] < HEIGHT)

    mask3 = src_auto_mask[kp1_np[:, 1].astype(np.int), kp1_np[:, 0].astype(np.int)] == 0
    mask4 = tgt_auto_mask[kp2_np[:, 1].astype(np.int), kp2_np[:, 0].astype(np.int)] == 0
    mask_src = mask1 * mask3
    mask_tgt = mask2 * mask4


    kp1, kp2, des1, des2 = [], [], [], []
    for i in range(len(kp1_ori)):
        if mask_src[i]:
            kp1.append(kp1_ori[i])
            des1.append(des1_ori[i])
    for i in range(len(kp2_ori)):
        if mask_tgt[i]:
            kp2.append(kp2_ori[i])
            des2.append(des2_ori[i])
    des1 = np.array(des1)
    des2 = np.array(des2)

    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    if len(matches[0]) < 2:
        return True, 0, 0


    # Apply ratio test
    good = []
    i = 0
    m_temp = matches[0][0]
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            if i == 0 or kp1[m_temp.queryIdx].pt != kp1[m.queryIdx].pt:
                good.append([m])
            else:
                if m_temp.distance > m.distance:
                    good.pop(-1)
                    good.append([m])
            i += 1
            m_temp = m
            # cv.drawMatchesKnn expects list of lists as matches.

    good_np = np.array([list([good[idx][0].queryIdx,good[idx][0].trainIdx]) for idx in range(0, len(good))])
    if len(good_np) == 0:
        return True, 0, 0
    kp1_np = np.array([list(kp1[idx].pt) for idx in range(0, len(kp1))])
    kp2_np = np.array([list(kp2[idx].pt) for idx in range(0, len(kp2))])
    kp1_good_np = kp1_np[good_np[:,0]]
    kp2_good_np = kp2_np[good_np[:,1]]

    Tx = np.array([[0, -T_gt[2,3], T_gt[1,3]], [T_gt[2,3], 0, -T_gt[0,3]], [-T_gt[1,3], T_gt[0,3], 0]])
    F = np.linalg.inv(tgt_K.transpose(1,0)) @   Tx @ T_gt[:3, :3] @ np.linalg.inv(src_K)


    lines1 = cv.computeCorrespondEpilines(kp2_good_np.reshape(-1,1,2), 2,F)
    lines1 = lines1.reshape(-1,3)
    distances1 = np.abs(lines1[:,0] * kp1_good_np[:,0] + lines1[:,1] * kp1_good_np[:,1] + lines1[:,2]) / np.sqrt(lines1[:,0]**2 + lines1[:,1]**2)

    lines2 = cv.computeCorrespondEpilines(kp1_good_np.reshape(-1,1,2), 1,F)
    lines2 = lines2.reshape(-1,3)
    distances2 = np.abs(lines2[:,0] * kp2_good_np[:,0] + lines2[:,1] * kp2_good_np[:,1] + lines2[:,2]) / np.sqrt(lines2[:,0]**2 + lines2[:,1]**2)

    distances = (distances1 + distances2) 

    kp_ransac_np = np.stack([kp1_good_np, kp2_good_np], axis=1)
    
    
    src_K_invert = np.linalg.inv(src_K)
    tgt_K_invert = np.linalg.inv(tgt_K)

    count = np.zeros(4)
    #pix_coord = np.zeros([4, kp_ransac_np.shape[0], 2])
    depth_ = np.zeros([4, kp_ransac_np.shape[0]])
    angle = np.zeros([4, kp_ransac_np.shape[0]])

    T_temp = T_gt
    T_invert = np.linalg.inv(T_temp)
    cam_points_0 = np.concatenate([kp_ransac_np[:,0,:], np.ones([kp_ransac_np.shape[0],1])],-1)
    cam_points_0 = np.dot(src_K_invert, cam_points_0.transpose(1,0))
    cam_points_1 = np.concatenate([kp_ransac_np[:,1,:], np.ones([kp_ransac_np.shape[0],1])],-1)
    cam_points_1 = np.dot(tgt_K_invert, cam_points_1.transpose(1,0))
    depth_0, angle_0 = compute_depth(cam_points_0.transpose(1,0), (np.dot(T_invert[:3,:3], cam_points_1)).transpose(1,0), T_invert[:3,3])
    depth_1, angle_1 = compute_depth(cam_points_1.transpose(1,0), (np.dot(T_temp[:3,:3], cam_points_0)).transpose(1,0), T_temp[:3,3])

    save0 = np.concatenate([kp_ransac_np[:, 0], depth_0[:, np.newaxis], angle_0[:, np.newaxis], distances1[:, np.newaxis], distances2[:, np.newaxis]], axis=-1)
    save1 = np.concatenate([kp_ransac_np[:, 1], depth_1[:, np.newaxis], angle_1[:, np.newaxis], distances1[:, np.newaxis], distances2[:, np.newaxis]], axis=-1)
    
    return False, save0, save1

def compute_depth(point_0, point_1, point_ori):
    x0 = 0
    y0 = 0
    z0 = 0
    cos_0 = point_0.copy()
    cos_0_norm = np.linalg.norm(cos_0, ord=2, axis=-1)
    cos_1 = (point_1).copy()
    cos_1_norm = np.linalg.norm(cos_1, ord=2, axis=-1)
    cos_value = (cos_0 * cos_1).sum(-1)/(cos_0_norm * cos_1_norm)
    cos_angle = np.arccos(cos_value)/np.pi*180
    x1 = point_ori[0]
    y1 = point_ori[1]
    z1 = point_ori[2]
    a0 = point_0[...,0]
    b0 = point_0[...,1]
    c0 = point_0[...,2]
    a1 = point_1[...,0]
    b1 = point_1[...,1]
    c1 = point_1[...,2]
    p0 = a0*(c0*a1 - a0*c1) - b0*(b0*c1 - c0*b1)
    p1 = -a1*(c0*a1 - a0*c1) + b1*(b0*c1 - c0*b1)
    q0 = a0*(a0*b1 - b0*a1) - c0*(b0*c1 - c0*b1)
    q1 = -a1*(a0*b1 - b0*a1) + c1*(b0*c1 - c0*b1)
    k0 = (y0 - y1)*(b0*c1 - c0*b1) - (x0 - x1)*(c0*a1 - a0*c1)
    k1 = (z0 - z1)*(b0*c1 - c0*b1) - (x0 - x1)*(a0*b1 - b0*a1)
    t0 = (q1*k0 - p1*k1)/(p0*q1 - q0*p1)
    depth = t0*c0
    return depth, cos_angle



data_path = '../data/nuscenes/raw_data'
version = 'v1.0-trainval'
nusc = NuScenes(version=version,
                dataroot=data_path, verbose=False)
with open('../datasets/nusc/train.txt', 'r') as f:
    info = f.readlines()

save_root_path = '../data/nuscenes/match'
root_path = '../data/nuscenes/sift'
camera_names = ['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT', 'CAM_FRONT_RIGHT']

for camera_name in camera_names:
    os.makedirs(os.path.join(save_root_path, 'samples', camera_name), exist_ok=True)

sift = cv.xfeatures2d.SIFT_create(edgeThreshold=8,contrastThreshold=0.01)
frame_ids = [-1, 1]


to_save_depth, to_save_pose = {}, {}

info_list = list(range(len(info)))
random.shuffle(info_list)

def process(source_id):
    start = time.time()
    rec = nusc.get('sample', info[source_id].strip())

    sifts, Ts, results, Ks = [], [], [], []
    break_flag = False
    for camera_id, camera_name in enumerate(camera_names):
        cam_sample = nusc.get('sample_data', rec['data'][camera_name])
        save_path = os.path.join(save_root_path, cam_sample['filename'][:-4] + '.pkl')
        if os.path.exists(save_path):
            break_flag = True
            break
        with open(os.path.join(root_path, cam_sample['filename'][:-4] + '.pkl'), 'rb') as f:
            source_sift = pickle.load(f)
            sifts.append(source_sift)
        

        ego_spatial = nusc.get(
                'calibrated_sensor', cam_sample['calibrated_sensor_token'])
            
        pose_0_spatial = Quaternion(ego_spatial['rotation']).transformation_matrix
        pose_0_spatial[:3, 3] = np.array(ego_spatial['translation'])
        

        Ts.append(pose_0_spatial)
        Ks.append(np.array(ego_spatial['camera_intrinsic']))
        results.append([])

    if break_flag:
        return

    for camera_id in range(len(camera_names)):

        mask_src = np.zeros((HEIGHT, WIDTH, 3))
        mask_tgt = np.zeros((HEIGHT, WIDTH, 3))
        mask_src[:, 500:, :] = 1
        mask_tgt[:, :-500, :] = 1

        #print(source_id, camera_id)
        flag, depth1, depth2 = compute_match(sifts[camera_id], sifts[(camera_id + 1)%6], \
            Ks[camera_id], Ks[(camera_id + 1)%6], \
            mask_src[...,0], mask_tgt[...,0], np.linalg.inv(Ts[(camera_id + 1)%6])@Ts[camera_id])
        
        if flag == 1:
            depth1 = np.ones((2,6))
            depth2 = np.ones((2,6))

        results[camera_id].append(depth1)
        results[(camera_id + 1)%6].append(depth2)

    for camera_id, camera_name in enumerate(camera_names):
        cam_sample = nusc.get('sample_data', rec['data'][camera_name])
        save_path = os.path.join(save_root_path, cam_sample['filename'][:-4] + '.pkl')

        results[camera_id] = np.concatenate(results[camera_id], axis=0)
        
        to_save = {'result': results[camera_id]}
        with open(save_path, 'wb') as f:
            pickle.dump(to_save, f)

    end = time.time()
    print(end - start, source_id)

p = multiprocessing.Pool(16)
p.map_async(process, info_list)
p.close()
p.join()

