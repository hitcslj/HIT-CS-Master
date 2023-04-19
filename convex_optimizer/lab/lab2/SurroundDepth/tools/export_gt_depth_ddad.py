import os
import scipy.io as sio
import sys
from dgp.datasets import SynchronizedSceneDataset
import json
import random
from tqdm import tqdm
import copy
import numpy as np
import pdb
import pickle

root_path = '../data/ddad/raw_data'
dataset =  SynchronizedSceneDataset(root_path + '/ddad.json',
                            datum_names=('CAMERA_01', 'CAMERA_05', 'CAMERA_06', 'CAMERA_07', 'CAMERA_08', 'CAMERA_09', 'lidar'),
                            generate_depth_from_datum='lidar',
                            split=sys.argv[1]
                        )

root_path = '../data/ddad/depth'
camera_names = ['CAMERA_01', 'CAMERA_05', 'CAMERA_06', 'CAMERA_07', 'CAMERA_08', 'CAMERA_09']

with open('../datasets/ddad/index.pkl', 'rb') as f:
    index_info = pickle.load(f)
to_save = {}

print(len(dataset))

for i in range(200):
    for camera_name in camera_names:
        os.makedirs(os.path.join(root_path, '{:06d}'.format(i), 'depth', camera_name), exist_ok=True)

count = 0
for data in tqdm(dataset):
    count += 1

    for i in range(6):
        m = data[0][i]
        t = str(m['timestamp'])
        save_temp = copy.deepcopy(m)
        if  t not in to_save.keys():
            to_save[t] = copy.deepcopy(index_info[t])

        scene_id = index_info[t]['scene_name']
        save_path = os.path.join(root_path, scene_id, 'depth', m['datum_name'], t + '.npy')
        np.save(save_path, m['depth'])

