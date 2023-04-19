import torch
import torch.nn as nn
import torch.nn.functional as F
import pdb
import math
import sys
import timm
# from timm.models.layers.mlp import Mlp
from timm.models.layers.helpers import to_2tuple
from timm.models.layers import trunc_normal_
import numpy as np


class CVT(nn.Module):
    def __init__(self,input_channel,downsample_ratio=2, iter_num=4):
        super().__init__()
        self.embed_dim = input_channel
        self.iter_num = iter_num
        self.self_block = []
        for i in range(iter_num):
            self.self_block.append(Self_Block(dim=self.embed_dim, num_heads=8))
        self.decoder = nn.ModuleList(list(self.self_block))
        
        self.postional_embed = PositionEmbeddingSine(num_pos_feats=self.embed_dim)
 
        self.downsample_ratio = downsample_ratio
        self.sep_conv = SeparableConv2d(in_channels=self.embed_dim,out_channels=self.embed_dim,stride=downsample_ratio)
        if downsample_ratio==16:
            kernel_size=3
            dilation = 7
            output_padding = 1
        elif downsample_ratio==8:
            kernel_size=3
            dilation = 3
            output_padding = 1
        elif downsample_ratio==4:
            kernel_size=3
            dilation = 1
            output_padding = 1
        elif downsample_ratio==2:
            kernel_size=1
            dilation = 1
            output_padding = 1
        elif downsample_ratio==1:
            kernel_size=1
            dilation = 1
            output_padding = 0
        self.sep_deconv = SeparableDeConv2d(in_channels=self.embed_dim,out_channels=self.embed_dim,stride=downsample_ratio, kernel_size = kernel_size, 
            dilation =dilation, output_padding=output_padding)


    def forward(self, x): # B, N, C, H, W
        B, N, C, H, W = x.shape
        x = self.sep_conv(x.view(-1,C,H,W)).view(B,N,C,H//self.downsample_ratio,W//self.downsample_ratio)

        for i in range(self.iter_num):
            self.pos_embed = self.postional_embed(x[:,0,:,:,:]).unsqueeze(1).repeat(1,N,1,1,1) # B, N, C, H, W
                
            # reshape #
            x = x.permute(0,1,3,4,2).reshape(B,-1,C)
            x_pos = self.pos_embed.permute(0,1,3,4,2).reshape(B,-1,C)
    
            x = self.self_block[i](x,x_pos).reshape(B,N,C,H//self.downsample_ratio, W//self.downsample_ratio)
    
        x = self.sep_deconv(x.view(-1, C, H//self.downsample_ratio, W//self.downsample_ratio))
        x = x.view(B,N,C,H,W)

        return x


class Self_Block(nn.Module):

    def __init__(self, dim, num_heads, mlp_ratio=4., qkv_bias=False, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm):
        super().__init__()
        self.norm1 = norm_layer(dim)
        self.attn = Self_Attention(dim, num_heads=num_heads, qkv_bias=qkv_bias, attn_drop=attn_drop, proj_drop=drop)
        # NOTE: drop path for stochastic depth, we shall see if this is better than dropout here
        self.drop_path = timm.models.layers.DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)

    def forward(self, x, x_pos):
        x = x + self.drop_path(self.attn(self.norm1(x),x_pos))
        x = x + self.drop_path(self.mlp(self.norm2(x)))
        return x

class Self_Attention(nn.Module):
    def __init__(self, dim, num_heads=8, qkv_bias=False, attn_drop=0., proj_drop=0.):
        super().__init__()
        assert dim % num_heads == 0, 'dim should be divisible by num_heads'
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim ** -0.5

        self.q_linear = nn.Linear(dim, dim, bias=qkv_bias)
        self.k_linear = nn.Linear(dim, dim, bias=qkv_bias)
        self.v_linear = nn.Linear(dim, dim, bias=qkv_bias)

        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, x,x_pos):
        B, N, C = x.shape

        q_vector = k_vector = x + x_pos
        v_vector = x

        q = self.q_linear(q_vector).reshape(B, N, self.num_heads, C // self.num_heads).permute(0, 2, 1, 3)
        k = self.k_linear(k_vector).reshape(B, N, self.num_heads, C // self.num_heads).permute(0, 2, 1, 3)
        v = self.v_linear(v_vector).reshape(B, N, self.num_heads, C // self.num_heads).permute(0, 2, 1, 3)

        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x


class SeparableConv2d(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size=1,stride=4,padding=0,dilation=1,bias=False):
        super(SeparableConv2d,self).__init__()

        self.conv1 = nn.Conv2d(in_channels,in_channels,kernel_size,stride,padding,dilation,groups=in_channels,bias=bias)
        self.pointwise = nn.Conv2d(in_channels,out_channels,1,1,0,1,1,bias=bias)
    
    def forward(self,x):
        x = self.conv1(x)
        x = self.pointwise(x)
        return x

class SeparableDeConv2d(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size=3,stride=4,padding=0,dilation=4,bias=False,output_padding=0):
        super(SeparableDeConv2d,self).__init__()

        self.conv1 = nn.ConvTranspose2d(in_channels, in_channels, kernel_size=kernel_size, stride=stride, groups=in_channels,padding=padding,dilation=dilation,
            output_padding=output_padding)
        self.pointwise = nn.Conv2d(in_channels,out_channels,1,1,0,1,1,bias=bias)
    
    def forward(self,x):
        # pdb.set_trace()
        x = self.conv1(x)
        x = self.pointwise(x)
        return x




class PositionEmbeddingSine(nn.Module):
    """
    This is a more standard version of the position embedding, very similar to the one
    used by the Attention is all you need paper, generalized to work on images.
    """
    def __init__(self, num_pos_feats=64, temperature=10000, normalize=False, scale=None):
        super().__init__()
        self.num_pos_feats = num_pos_feats // 2
        self.temperature = temperature
        self.normalize = normalize
        if scale is not None and normalize is False:
            raise ValueError("normalize should be True if scale is passed")
        if scale is None:
            scale = 2 * math.pi
        self.scale = scale

    def forward(self, x):
        # pdb.set_trace()
        # x = x.permute(0,2,3,1)
        mask = torch.zeros_like(x[:,0,:,:]).bool()
        assert mask is not None
        not_mask = ~mask
        y_embed = not_mask.cumsum(1, dtype=torch.float32)
        x_embed = not_mask.cumsum(2, dtype=torch.float32)
        if self.normalize:
            eps = 1e-6
            y_embed = y_embed / (y_embed[:, -1:, :] + eps) * self.scale
            x_embed = x_embed / (x_embed[:, :, -1:] + eps) * self.scale
        dim_t = torch.arange(self.num_pos_feats, dtype=torch.float32, device=x.device)
        dim_t = self.temperature ** (2 * (dim_t // 2) / self.num_pos_feats)
        # pdb.set_trace()
        pos_x = x_embed[:, :, :, None] / dim_t
        pos_y = y_embed[:, :, :, None] / dim_t
        pos_x = torch.stack((pos_x[:, :, :, 0::2].sin(), pos_x[:, :, :, 1::2].cos()), dim=4).flatten(3)
        pos_y = torch.stack((pos_y[:, :, :, 0::2].sin(), pos_y[:, :, :, 1::2].cos()), dim=4).flatten(3)
        pos = torch.cat((pos_y, pos_x), dim=3).permute(0, 3, 1, 2)
        return pos

class Mlp(nn.Module):
    """ MLP as used in Vision Transformer, MLP-Mixer and related networks
    """
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0.):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        drop_probs = to_2tuple(drop)

        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = act_layer()
        self.drop1 = nn.Dropout(drop_probs[0])
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop2 = nn.Dropout(drop_probs[1])

    def forward(self, x):
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop1(x)
        x = self.fc2(x)
        x = self.drop2(x)
        return x
