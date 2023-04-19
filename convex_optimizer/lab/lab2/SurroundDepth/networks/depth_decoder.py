# Copyright Niantic 2019. Patent Pending. All rights reserved.
#
# This software is licensed under the terms of the Monodepth2 licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.

from __future__ import absolute_import, division, print_function

import numpy as np
import torch
import torch.nn as nn

from collections import OrderedDict
from layers import *
from .transformer import *


class DepthDecoder(nn.Module):
    def __init__(self, opt, num_ch_enc, scales=range(4), num_output_channels=1, use_skips=True):
        super(DepthDecoder, self).__init__()

        self.opt = opt
        self.num_output_channels = num_output_channels
        self.upsample_mode = 'nearest'
        self.scales = scales
        self.use_skips = use_skips

        
        self.iter_num = [8, 8, 8, 8, 8]
        self.num_ch_enc = num_ch_enc
        self.num_ch_dec = np.array([16, 32, 64, 128, 256])

        # decoder
        self.convs = OrderedDict()
        for i in range(4, -1, -1):
            # upconv_0
            num_ch_in = self.num_ch_enc[-1] if i == 4 else self.num_ch_dec[i + 1]
            num_ch_out = self.num_ch_dec[i]
            self.convs[("upconv", i, 0)] = ConvBlock(num_ch_in, num_ch_out)


            # upconv_1
            num_ch_in = self.num_ch_dec[i]
            if self.use_skips and i > 0:
                num_ch_in += self.num_ch_enc[i - 1]
            num_ch_out = self.num_ch_dec[i]
            self.convs[("upconv", i, 1)] = ConvBlock(num_ch_in, num_ch_out)


        for s in self.scales:
            self.convs[("dispconv", s)] = Conv3x3(self.num_ch_dec[s], self.num_output_channels)

        self.decoder = nn.ModuleList(list(self.convs.values()))
        self.sigmoid = nn.Sigmoid()

        self.cross = {}

        for i in range(len(self.num_ch_enc)):
            self.cross[i] = CVT(input_channel=self.num_ch_enc[i], downsample_ratio=2**(len(self.num_ch_enc) -1 - i), iter_num=self.iter_num[i])

        self.decoder_cross = nn.ModuleList(list(self.cross.values()))

    def forward(self, input_features):
        self.outputs = {}
        for i in range(len(input_features)):
            B, C, H, W = input_features[i].shape
            if self.opt.skip:
                input_features[i] = input_features[i] + self.cross[i](input_features[i].reshape(-1, 6, C, H, W)).reshape(B, C, H, W)
            else:
                input_features[i] = self.cross[i](input_features[i].reshape(-1, 6, C, H, W)).reshape(B, C, H, W)
        
        # decoder
        x = input_features[-1]
        for i in range(4, -1, -1):
            x = self.convs[("upconv", i, 0)](x)
            x = [upsample(x)]
            if self.use_skips and i > 0:
                x += [input_features[i - 1]]
            x = torch.cat(x, 1)
            x = self.convs[("upconv", i, 1)](x)
            if i in self.scales:
                self.outputs[("disp", i)] = self.sigmoid(self.convs[("dispconv", i)](x))

        return self.outputs
