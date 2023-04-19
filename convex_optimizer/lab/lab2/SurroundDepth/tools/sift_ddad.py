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


def _pickle_keypoints(point):
    return cv.KeyPoint, (*point.pt, point.size, point.angle,
                         point.response, point.octave, point.class_id)
copyreg.pickle(cv.KeyPoint().__class__, _pickle_keypoints)

root_path = '../data/ddad/sift'
rgb_path = '../data/ddad/raw_data'
camera_names = ['CAMERA_01', 'CAMERA_05', 'CAMERA_06', 'CAMERA_07', 'CAMERA_08', 'CAMERA_09']
sift = cv.xfeatures2d.SIFT_create(edgeThreshold=8,contrastThreshold=0.01)

with open('../datasets/ddad/info_train.pkl', 'rb') as f:
    info = pickle.load(f)


def process(frame_id):
    scene_name = info[frame_id]['scene_name']
    for camera_name in camera_names:
        to_save = {}
        os.makedirs(os.path.join(root_path, scene_name, 'sift', camera_name), exist_ok=True)
        save_path = os.path.join(root_path, scene_name, 'sift', 
                                camera_name, frame_id + '.pkl')
        if os.path.exists(save_path):
            continue
        print(frame_id, camera_name)
        inputs = cv.imread(os.path.join(rgb_path, scene_name, 'rgb', 
                                camera_name, frame_id + '.png'))
        img1 = cv.cvtColor(inputs, cv.COLOR_RGB2GRAY)
        kp1, des1 = sift.detectAndCompute(img1,None)
        to_save['kp'] = kp1
        to_save['des'] = des1

        
        with open(save_path, 'wb') as f:
            pickle.dump(to_save, f)
    
        
p = multiprocessing.Pool(8)
info_list = info.keys()
p.map_async(process, info_list)
p.close()
p.join()