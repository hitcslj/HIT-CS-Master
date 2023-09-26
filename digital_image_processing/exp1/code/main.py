import numpy as np
import struct
import matplotlib.pyplot as plt
import math
import pandas as pd


# 参考：https://blog.csdn.net/qq_43409114/article/details/104538619
def readinfo(file_path=None):
    '先将位图打开'
    f = open(file_path, 'rb')  # 打开对应的文件

    '下面部分用来读取BMP位图的基础信息'
    f_type = str(f.read(2))  # 这个就可以用来读取 文件类型 需要读取2个字节
    file_size_byte = f.read(4)  # 这个可以用来读取文件的大小 需要读取4个字节
    f.seek(f.tell() + 4)  # 跳过中间无用的四个字节
    file_ofset_byte = f.read(4)  # 读取位图数据的偏移量
    f.seek(f.tell() + 4)  # 跳过无用的两个字节
    file_wide_byte = f.read(4)  # 读取宽度字节
    file_height_byte = f.read(4)  # 读取高度字节
    f.seek(f.tell() + 2)  ## 跳过中间无用的两个字节
    file_bitcount_byte = f.read(4)  # 得到每个像素占位大小

    # 下面就是将读取的字节转换成指定的类型
    f_size, = struct.unpack('l', file_size_byte)
    f_ofset, = struct.unpack('l', file_ofset_byte)
    f_wide, = struct.unpack('l', file_wide_byte)
    f_height, = struct.unpack('l', file_height_byte)
    f_bitcount, = struct.unpack('i', file_bitcount_byte)
    print("类型:", f_type, "大小:", f_size, "位图数据偏移量:", f_ofset, "宽度:", f_wide, "高度:", f_height, "位图:", f_bitcount)

    '然后来读取颜色表'
    color_table = np.empty(shape=[256, 3], dtype=int)
    f.seek(54)  # 跳过文件信息头和位图信息头
    for i in range(0, 256):
        b = struct.unpack('B', f.read(1))[0];
        g = struct.unpack('B', f.read(1))[0];
        r = struct.unpack('B', f.read(1))[0];
        alpha = struct.unpack('B', f.read(1))[0];
        color_table[i][0] = r
        color_table[i][1] = g
        color_table[i][2] = b
    '下面部分用来读取BMP位图数据区域,将数据存入numpy数组'
    # 首先对文件指针进行偏移
    f.seek(f_ofset)
    # 因为图像是8位伪彩色图像，所以一个像素点占一个字节，即8位
    img = np.empty(shape=[f_height, f_wide, 3], dtype=int)
    cout = 0
    for y in range(0, f_height):
        for x in range(0, f_wide):
            cout = cout + 1
            index = struct.unpack('B', f.read(1))[0]
            img[f_height - y - 1, x] = color_table[index]
        while cout % 4 != 0:
            f.read(1)
            cout = cout + 1
    plt.imshow(img)
    plt.show()
    f.close()
    return img.astype(np.uint8)


def calHist(img_array,channel=0):
    '''

    :param img_array: 图像numpy数组，[h,w,c]
    :param channel:
    :return:
    '''
    assert 0<=channel<3
    print(img_array.shape)  # 打印图像的大小
    print(img_array.max(), img_array.min())  # 打印图片的灰度值的最大值和最小值
    gray_hist = np.zeros(img_array.max() + 1)  # 直方图的维度为最大灰度值加1

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            gray_hist[img_array[i][j][channel]] += 1  # 统计图片中，每个灰度值的个数

    print(gray_hist.max(), gray_hist.min())  # 展示灰度直方图中的最大值和最小值
    plt.plot(gray_hist)  # 画灰度直方图
    plt.title('example histogram ')
    plt.xlabel('grayscale value ')
    plt.ylabel('Pixel values ')
    plt.show()

def plotImg(img,name='RGB'):
    _, axs = plt.subplots(2, 2)
    plt.suptitle(name)
    axs[0][0].imshow(img.astype(np.uint8))
    a,b,c = img.transpose(2,0,1)
    axs[0][1].imshow(a, cmap=plt.cm.gray)
    axs[1][0].imshow(b, cmap=plt.cm.gray)
    axs[1][1].imshow(c, cmap=plt.cm.gray)
    plt.show()

def rgb2rgb(img):
    plotImg(img,name='RGB')

def rgb2ycbcr(rgb_image):
    """convert rgb into ycbcr"""
    if len(rgb_image.shape)!=3 or rgb_image.shape[2]!=3:
        raise ValueError("input image is not a rgb image")
    rgb_image = rgb_image.astype(np.float32)
    # 1：创建变换矩阵，和偏移量
    transform_matrix = np.array([[0.257, 0.564, 0.098],
                                 [-0.148, -0.291, 0.439],
                                 [0.439, -0.368, -0.071]])
    shift_matrix = np.array([16, 128, 128])
    ycbcr_image = np.zeros(shape=rgb_image.shape)
    w, h, _ = rgb_image.shape
    # 2：遍历每个像素点的三个通道进行变换
    for i in range(w):
        for j in range(h):
            ycbcr_image[i, j, :] = np.dot(transform_matrix, rgb_image[i, j, :]) + shift_matrix
    plotImg(ycbcr_image,name='YCbCr')



def rgb2xyz(img):
    r,g,b = img.transpose(2,0,1)
    x = 0.49 * r + 0.31 * g + 0.2 * b
    y = 0.177 * r + 0.813 * g + 0.011 * b
    z = 0.01 * g + 0.99 * b
    xyz_img = np.zeros(shape=img.shape)
    xyz_img[:, :, 0] = x
    xyz_img[:, :, 1] = y
    xyz_img[:, :, 2] = z
    plotImg(xyz_img,name='XYZ')




def rgb2yiq(img):
    r, g, b = img.transpose(2,0,1)
    y = 0.30 * r + 0.59 * g + 0.11 * b
    i = 0.74 * (r - y) - 0.27 * (b - y)
    q = 0.48 * (r - y) + 0.41 * (b - y)
    yiq_img = np.zeros(shape=img.shape)
    yiq_img[:,:,0] = y
    yiq_img[:,:,1] = i
    yiq_img[:,:,2] = q
    plotImg(yiq_img,"YIQ")


def rgb2hsi(img):
    R, G, B = img.transpose(2,0,1)
    up = 0.5*((R-G)+(R-B))+1e-3
    x = (np.multiply((R - B), (G - B)))
    down = np.multiply((R-G),(R-G))+np.sqrt(x)+1e-3
    theta = np.arccos(np.divide(up,down))
    temp = B>G
    H = np.multiply(temp*(-2)-2,theta)+theta*(3)+temp*360
    I = (R+G+B)/3
    S = 1-np.divide(np.min((R,G,B),axis=0)+1e-4,I+1e-4)
    hsi_img = np.zeros(shape=img.shape)
    hsi_img[:, :, 0] = H
    hsi_img[:, :, 1] = S
    hsi_img[:, :, 2] = I
    plotImg(hsi_img, name='HSI')

# def PermutationFun(inputImage, blockwidth=16, blockheight=16,seed=0):
#     """
#     实现图像按照指定块划分，并置乱块的位置显示图像，然后尝试恢复置乱后的图像
#     :param file_path: 文件路径（相对路径读不出来，绝对路径可以读出来，使用了绝对路径）
#     :return: 无返回
#     """
#
#     img = inputImage.copy()
#     # 显示某个位置上的像素值
#     print("Please input the position where you want to show.")
#     position_x, position_y = 0,0  # position_x,position_y = map(int,input().split(','))
#
#     img_val = img[position_x, position_y, :]
#
#     print("Position[", position_x, ',', position_y, "]'s pixel value is", img_val)
#
#     # # 图像分成任意块大小，并置交换某两块之间的位置
#     # size = random.randint(4, 8)
#     # sub_img_0_0 = img[0:size, 0:size, :]
#     # sub_img_40_40 = img[40 * size:41 * size, 40 * size:41 * size, :]
#     # print("图片分块的大小为", size)
#     # print("交换位置在[0, 0]和[", 40 * size, ",", 40 * size, "]的分块")
#     # temp_sub_img = sub_img_0_0.copy()
#     # img2 = img.copy()
#     # img2[0:size, 0:size, :] = sub_img_40_40
#     # img2[40 * size:41 * size, 40 * size:41 * size, :] = temp_sub_img
#
#     # plotImg(img2,'transform')
#
#     # 指定区域内(0,0)到(400,400)的图像分块并置乱块的大小
#     # print("将图片(0,0)到(400,400)的部分进行分块，请输入分块大小:")
#
#     # assert 0 < blockwidth <= img.shape[1] and 0<blockheight<=img.shape[0]
#     # # 这里只实现正方形切割,长方形类似
#     sub_size = 64 #4,8,16,32,64 int(input())
#     sub_img = np.zeros((math.ceil(512 / sub_size), math.ceil(512 / sub_size), sub_size, sub_size, 3))
#     padding_img = np.zeros((512,512,3),dtype=int)
#
#     padding_img[:img.shape[0],:img.shape[1],:] = img[:,:,:]
#
#     plotImg(padding_img,'image_padding')
#     mpt = []
#     idx = 0
#     for i in range(0, math.ceil(512 / sub_size)):
#         for j in range(0, math.ceil(512 / sub_size)):
#             sub_img[i, j] = (padding_img[i * sub_size:(i + 1) * sub_size, j * sub_size:(j + 1) * sub_size, :])
#             mpt.append((i,j))
#             idx+=1
#     random.shuffle(mpt)
#     idx = 0
#     shuffle_img = np.zeros((512,512,3),dtype=int)
#     for i in range(0, math.ceil(512 / sub_size)):
#         for j in range(0, math.ceil(512 / sub_size)):
#             x,y = mpt[idx]
#             idx += 1
#             shuffle_img[i * sub_size:(i + 1) * sub_size, j * sub_size:(j + 1) * sub_size, :]=sub_img[x][y]
#     plotImg(shuffle_img,'shuffle')
#     # 其实原本是要根据打乱图来恢复的，但用网络硬训一个太麻烦了，这里写了一个假的。
#     restore_img = np.zeros((512, 512, 3), dtype=int)
#     for i in range(0, math.ceil(512 / sub_size)):
#         for j in range(0, math.ceil(512 / sub_size)):
#             restore_img[i * sub_size:(i + 1) * sub_size, j * sub_size:(j + 1) * sub_size, :] = sub_img[i][j]
#     plotImg(restore_img, 'fix_img')


def PermutationFun(image, block_width, block_height, swap_mode,seed=3):

    height,width= image.shape[:2]
    b_row = int((height-1)/block_height)+1
    b_col = int((width-1)/block_width)+1
    b_row = max(b_row,b_col)
    b_col = b_row

    imagetemp = np.zeros((b_row*block_height,b_col*block_width,image.shape[2])).astype(np.uint8)
    imagetemp[:height,:width,:] = image
    image = imagetemp

    image_swap = np.zeros((b_row*block_height,b_col*block_width,image.shape[2])).astype(np.uint8)

    loc_index = np.zeros((2,1))
    index_mod = np.array([[b_row],[b_col]])
    for i in range(b_row):
        for j in range(b_col):
            loc_index[0][0]=i
            loc_index[1][0]=j
            swap_index = loc_index
            for _ in range(seed):
                swap_index = np.matmul(swap_mode,swap_index)
            swap_index = np.mod(swap_index,index_mod).astype(np.uint8)
            y= i*block_height
            x= j*block_width
            y_s = swap_index[0][0] * block_height
            x_s = swap_index[1][0] * block_width
            #assert image_swap[y_s][x_s][1]==0
            image_swap[y_s:(y_s+block_height),x_s:(x_s+block_width),:] = image[y:(y+block_height),x:(x+block_width),:]
    return image_swap.astype(np.uint8)

def Permutation_rigon(image,block_width,block_height, swap_mode,rigon):#rigon((x1,y1),(x2,y2))
    height_i,width_i = image.shape[:2]
    assert rigon[0][0]<rigon[1][0]
    assert rigon[0][1]<rigon[1][1]
    assert rigon[1][0]<=width_i
    assert rigon[0][0]>=0
    assert rigon[1][1]<=height_i
    assert rigon[0][1]>=0
    image_swap = PermutationFun(image[rigon[0][1]:rigon[1][1],rigon[0][0]:rigon[1][0],:],block_width,block_height,swap_mode)
    b_row = int(((rigon[1][1]-rigon[0][1]) - 1) / block_height) + 1
    b_col = int(((rigon[1][0]-rigon[0][0]) - 1) / block_width) + 1
    b_row = max(b_row,b_col)
    b_col = b_row

    image_rigon = np.zeros((height_i-(rigon[1][1]-rigon[0][1])+b_row*block_height,width_i-(rigon[1][0]-rigon[0][0])+b_col*block_width,image.shape[2]))
    image_rigon[:rigon[0][1],:rigon[1][0],:]=image[:rigon[0][1],:rigon[1][0],:]
    image_rigon[:rigon[0][1],(b_col*block_width+rigon[0][0]):,:]=image[:rigon[0][1],rigon[1][0]:,:]
    image_rigon[:rigon[1][1],:rigon[0][0],:]=image[:rigon[1][1],:rigon[0][0],:]
    image_rigon[rigon[0][1]:(b_row*block_height+rigon[0][1]),rigon[0][0]:(b_col*block_width+rigon[0][0]),:]=image_swap
    image_rigon[:rigon[1][1],(b_col*block_width+rigon[0][0]):,:]=image[:rigon[1][1],rigon[1][0]:,:]

    image_rigon[(b_row*block_height+rigon[0][1]):, :rigon[1][0], :] = image[rigon[1][1]:, :rigon[1][0], :]
    image_rigon[(b_row*block_height+rigon[0][1]):, (b_col * block_width + rigon[0][0]):, :] = image[rigon[1][1]:, rigon[1][0]:, :]
    return image_rigon.astype(np.uint8)

def dePermutation(image,block_width,block_height, swap_mode,seed=3):
    de_swap_mode = np.linalg.inv(swap_mode)
    #image_ori = PermutationFun(image,block_width,block_height,de_swap_mode)
    height, width = image.shape[:2]
    b_row = int(height / block_height)
    b_col = int(width /block_width)

    image_swap = np.zeros((b_row * block_height, b_col * block_width, image.shape[2]))

    loc_index = np.zeros((2, 1))
    index_mod = np.array([[b_row], [b_col]])
    for i in range(b_row):
        for j in range(b_col):
            loc_index[0][0] = i
            loc_index[1][0] = j
            swap_index = loc_index
            for _ in range(seed):
                swap_index = np.matmul(de_swap_mode, swap_index)
            swap_index = np.mod(swap_index, index_mod).astype(np.uint8)
            y = i * block_height
            x = j * block_width
            y_s = swap_index[0][0] * block_height
            x_s = swap_index[1][0] * block_width
            image_swap[y_s:(y_s + block_height), x_s:(x_s + block_width), :] = image[y:(y + block_height),
                                                                               x:(x + block_width), :]

    return image_swap.astype(np.uint8)


def psnr(target, ref):
    # target:目标图像  ref:参考图像
    # assume RGB image
    if not target.shape == ref.shape:
        raise ValueError("Input Imagees must have the same dimensions")
    if len(target.shape) > 2:
        raise ValueError("Please input the images with 1 channel")
    target_data = np.array(target)
    ref_data = np.array(ref)
    diff = ref_data - target_data
    diff = diff.flatten('C')
    rmse = math.sqrt(np.mean(diff ** 2.)) + 1e-5
    return 10*math.log((255**2/rmse),10)


def calcov(x,y):
    total = 1
    for i in y.shape:
        total = total * i
    mean_y = np.mean(y)
    mean_x = np.mean(x)
    return np.sum(np.multiply(x,y))/total-mean_y*mean_x

def compute_ssim(x, y):

    ux = np.mean(x)
    uy = np.mean(y)

    dxy = calcov(x, y)
    dx = calcov(x, x)
    dy = calcov(y, y)
    c1 = 1
    c2 = 2
    up = (2 * ux * uy + c1) * (2 * dxy + c2)
    down = (ux ** 2 + uy ** 2 + c1) * (dx + dy + c2)
    return up / down





def gaussian_noise(img, mean=0, sigma=1):
    '''
    此函数用将产生的高斯噪声加到图片上
    传入:
        img   :  原图
        mean  :  均值
        sigma :  标准差
    返回:
        gaussian_out : 噪声处理后的图片
        noise        : 对应的噪声
    '''
    # 将图片灰度标准化
    img = img / 255
    # 产生高斯 noise
    noise = np.random.normal(mean, sigma, img.shape)
    # 将噪声和图片叠加
    gaussian_out = img + noise
    # 将超过 1 的置 1，低于 0 的置 0
    gaussian_out = np.clip(gaussian_out, 0, 1)
    # 将图片灰度范围的恢复为 0-255
    gaussian_out = np.uint8(gaussian_out*255)
    # 将噪声范围搞为 0-255
    # noise = np.uint8(noise*255)
    return img,gaussian_out, noise # 这里也会返回噪声，注意返回值


from collections import Counter
def find_color():
    img = readinfo('test.bmp')
    cnt = Counter()
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            cnt[(img[x][y][0],img[x][y][1],img[x][y][2])]+=1
    print(len(cnt))
    return len(cnt)

from collections import defaultdict


#参考https://blog.csdn.net/qq_43741312/article/details/97128745
class Cluster():
    def __init__(self,dataSet,k,episode = 100):
        self.dataset = dataSet.astype(np.int32)
        centroids = set()
        for r,g,b in dataSet:
            centroids.add((r,g,b))
            if len(centroids) == k:
                break
        assert len(centroids)==k
        self.centroids = [[r,g,b] for r,g,b in centroids]
        self.k = k
        self.episode = episode

    # 计算欧拉距离
    def calcDis(self,centroids, k):
        dataSet = self.dataset
        clalist = []
        for data in dataSet:
            diff = np.tile(data, (k,1)) - centroids  # 相减   (np.tile(a,(2,1))就是把a先沿x轴复制1倍，即没有复制，仍然是 [0,1,2]。 再把结果沿y方向复制2倍得到array([[0,1,2],[0,1,2]]))
            squaredDiff = np.power(diff,2)  # 平方
            squaredDist = np.sum(squaredDiff, axis=1)  # 和  (axis=1表示行)
            distance = squaredDist ** 0.5  # 开根号
            clalist.append(distance)
        clalist = np.array(clalist)  # 返回一个每个点到质点的距离len(dateSet)*k的数组
        return clalist

    # 计算质心
    def classify(self, centroids, k):
        # 计算样本到质心的距离
        dataSet = self.dataset
        clalist = self.calcDis(centroids, k)
        # 分组并计算新的质心
        minDistIndices = np.argmin(clalist, axis=1)  # axis=1 表示求出每行的最小值的下标
        newCentroids = pd.DataFrame(dataSet).groupby(
            minDistIndices).mean()  # DataFramte(dataSet)对DataSet分组，groupby(min)按照min进行统计分类，mean()对分类结果求均值
        newCentroids = np.array(newCentroids.values,np.uint8)

        # 计算变化量
        changed = newCentroids - centroids

        return changed, newCentroids

    # 使用k-means分类
    def kmeans(self):
        # 随机取质心
        dataSet = self.dataset
        k = self.k
        centroids = self.centroids

        # 更新质心 直到变化量全为0
        changed, newCentroids = self.classify(centroids, k)
        loop = 1
        while np.any(changed != 0) and loop<self.episode:
            changed, newCentroids = self.classify(newCentroids, k)
            loop+=1

        centroids = sorted(newCentroids.tolist())  # tolist()将矩阵转换成列表 sorted()排序

        # 根据质心计算每个集群
        cluster = []
        clalist = self.calcDis(centroids, k)  # 调用欧拉距离
        # print('clalist.shape:', clalist.shape)
        minDistIndices = np.argmin(clalist, axis=1)
        for i in range(k):
            cluster.append([])
        mpt = defaultdict(list)
        for i, j in enumerate(minDistIndices):  # enumerate()可同时遍历索引和遍历元素
            mpt[tuple(dataSet[i])]=centroids[j]
            cluster[j].append(dataSet[i])

        return centroids, cluster,mpt



def BMP_GIF(picture , k=256):
    image = readinfo(picture)
    image_color = np.resize(image, (image.shape[0] * image.shape[1], image.shape[2]))

    episode = 1
    centroids, cluster,mpt = Cluster(image_color, k,episode).kmeans()
    file = open(picture, "rb").read()
    gif_img = np.zeros_like(image)
    for x in range(gif_img.shape[0]):
        for y in range(gif_img.shape[1]):
            gif_img[x][y]=mpt[tuple(image[x][y])]
    plotImg(gif_img, 'cluster')
    # gif_img = Image.fromarray(gif_img)
    # gif_img.save('git_test.bmp','bmp')

if __name__ == '__main__':
    # # 读取bmp文件并显示，返回 numpy array
    # img = readinfo(file_path='test.bmp')
    # # 统计灰度直方图
    # calHist(img,channel=0)
    #
    # # rgb转换
    # rgb2rgb(img)
    # rgb2hsi(img)
    # rgb2yiq(img)
    # rgb2xyz(img)
    # rgb2ycbcr(img)
    #
    #
    # # 置乱块
    # block_height = 20
    # block_width = 20
    # seed = 6
    # SWAP_MODE = np.array([[1, 1], [1, 2]])
    # image = loadBMP('test.bmp')
    # image_swap = PermutationFun(image, block_width, block_height, SWAP_MODE, seed)
    # plt.imshow(image_swap)
    # plt.show()
    # image_ori = dePermutation(image_swap, block_width, block_height, SWAP_MODE, seed)
    # plt.imshow(image_ori)
    # plt.show()
    #
    # image_rigon = Permutation_rigon(image, block_width, block_height, SWAP_MODE, ((20, 20), (120, 120)))
    # plt.imshow(image_rigon)
    # plt.show()

    # # 计算PSNP,SSIM
    # clean_img,noisy_img,_ = gaussian_noise(img[:,:,0])
    # plt.imshow(clean_img)
    # plt.show()
    # plt.imshow(noisy_img)
    # plt.show()
    # print('psnr: ',psnr(clean_img,noisy_img))
    # print('ssim: ',compute_ssim(clean_img,noisy_img))

    # 将BMP图像转化为GIF图像
    # find_color() #统计出来原始test.tmp只有58种颜色 图片是8bit的位图
    BMP_GIF('test.bmp',k=58)



