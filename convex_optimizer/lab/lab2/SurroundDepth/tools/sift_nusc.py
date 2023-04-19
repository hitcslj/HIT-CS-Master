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
import pickle
from tqdm import tqdm
import copyreg
import time
import multiprocessing

from nuscenes.nuscenes import NuScenes
from pyquaternion import Quaternion
import random


def _pickle_keypoints(point):
    return cv.KeyPoint, (*point.pt, point.size, point.angle,
                         point.response, point.octave, point.class_id)
copyreg.pickle(cv.KeyPoint().__class__, _pickle_keypoints)


data_path = '../data/nuscenes/raw_data'
version = 'v1.0-trainval'
nusc = NuScenes(version=version,
                dataroot=data_path, verbose=False)
with open('../datasets/nusc/train.txt', 'r') as f:
    info = f.readlines()

save_root_path = '../data/nuscenes/sift'
camera_names = ['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT', 'CAM_FRONT_RIGHT']

for camera_name in camera_names:
    os.makedirs(os.path.join(save_root_path, 'samples', camera_name), exist_ok=True)

sift = cv.xfeatures2d.SIFT_create(edgeThreshold=8,contrastThreshold=0.01)

info_list = list(range(len(info)))
random.shuffle(info_list)

def process(frame_id):
    rec = nusc.get('sample', info[frame_id].strip())
    for camera_name in camera_names:
        cam_sample = nusc.get('sample_data', rec['data'][camera_name])
        to_save = {}
        save_path = os.path.join(save_root_path, cam_sample['filename'][:-4] + '.pkl')
        if os.path.exists(save_path):
            continue
        inputs = cv.imread(os.path.join(data_path, cam_sample['filename']))
        img1 = cv.cvtColor(inputs, cv.COLOR_RGB2GRAY)
        kp1, des1 = sift.detectAndCompute(img1,None)
        to_save['kp'] = kp1
        to_save['des'] = des1
        print(cam_sample['filename'], camera_name)

        
        with open(save_path, 'wb') as f:
            pickle.dump(to_save, f)
    
        
p = multiprocessing.Pool(8)

p.map_async(process, info_list)
p.close()
p.join()
