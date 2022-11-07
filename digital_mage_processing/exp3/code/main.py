import numpy as np
from PIL import Image
from imageio import imsave
import matplotlib.pyplot as plt
import math
import pywt

def loadpicture(file):
    image=Image.open(file)
    return np.array(image)


# 参考：https://blog.csdn.net/Ibelievesunshine/article/details/104922449
# histogram equalization
def hist_equal(img, z_max=255):
    H, W = img.shape
    # S is the total of pixels
    S = H * W * 1.

    out = img.copy()

    sum_h = 0.

    for i in range(1, 255):
        ind = np.where(img == i)
        sum_h += len(img[ind])
        z_prime = z_max / S * sum_h
        out[ind] = z_prime

    out = out.astype(np.uint8)

    return out


def SaltPapperNoist(image, prob):
    height,width,channel = image.shape
    noistnumber = int(height*width*channel*prob)
    image = np.array(image)
    for _ in range(noistnumber):
        row = np.random.randint(0,height)
        col = np.random.randint(0,width)
        c = np.random.randint(0,channel)
        if np.random.random()<0.1:
            image[row][col][c] = 0
        else:
            image[row][col][c] = 255
    return image
def GaussiNois(image ,mean, sigma):
    noise = np.random.normal(mean,sigma,image.shape)
    image = np.array(image)
    image = image+noise
    image = np.clip(image, 0, 255).astype(np.uint8)
    return image

def middleFilter(image , size=3):
    middle_index = int(size*size/2)+1
    row,col,channel = image.shape
    image_pad = np.zeros((row+size-1,col+size-1,channel),dtype=np.uint8)
    image_file = np.zeros(image.shape)
    image_pad[:image.shape[0],:image.shape[1],:image.shape[2]] = image

    Hs=[]
    nms=[]
    middles=[]
    for c in range(channel):
        H_c = []
        for _ in range(257):
            H_c.append(0)
        sortlist = []
        for _ in range(size):
            sortlist.append(0)
        for i in range(size-1):
            for j in range(size):
                sortlist.append(image_pad[i][j][c])
        sortlist.sort()
        middles.append(sortlist[middle_index-1])
        nm = 0
        pre_pix = -1
        sortlist_temp = []
        for x in sortlist:
            if x==pre_pix:
                continue
            else:
                sortlist_temp.append(x)
                pre_pix = x
                H_c[x] = sortlist.count(x)
                if x <= middles[c]:
                    nm += sortlist.count(x)
        Hs.append(H_c)
        nms.append(nm)
    base = size-1
    row_num = int(row/2)
    for i in range(row_num):
        i_base = i * 2
        for c in range(channel):
            for a in range(size):
                if image_pad[i_base-1][a][c] <= middles[c]:
                    nms[c] -= 1
                Hs[c][image_pad[i_base-1][a][c]] -=1
                if image_pad[i_base-1+ size][a][c] <= middles[c]:
                    nms[c] += 1
                Hs[c][image_pad[i_base-1+ size][a][c] ]+=1

            if nms[c] > middle_index:
                while nms[c] > middle_index:
                    nms[c] -= Hs[c][middles[c]]
                    middles[c] -= 1
                if nms[c] < middle_index:
                    middles[c]+=1
                    nms[c] += Hs[c][middles[c]]
                image_file[i_base][j - base][c] = middles[c]
            elif nms[c] < middle_index:
                while nms[c] < middle_index:
                    middles[c] += 1
                    nms[c] += Hs[c][middles[c]]
                image_file[i_base][j - base][c] = middles[c]
            else:
                image_file[i_base][j - base][c] = middles[c]

        for j in range(base+1,col+base):
            i_base = i*2
            for c in range(channel):
                for a in range(size):
                    if image_pad[i_base+a][j-size][c]<=middles[c]:
                        nms[c]-=1
                    Hs[c][image_pad[i_base+a][j-size][c]] -= 1
                    if image_pad[i_base+a][j][c]<=middles[c]:
                        nms[c]+=1
                    Hs[c][image_pad[i_base+a][j][c]]+=1
                if nms[c]> middle_index:
                    while nms[c]>middle_index:
                        nms[c] -= Hs[c][middles[c]]
                        middles[c] -= 1
                    if nms[c] < middle_index:
                        middles[c] += 1
                        nms[c] += Hs[c][middles[c]]
                    image_file[i_base][j-base][c] = middles[c]
                elif nms[c] < middle_index:
                    while nms[c] < middle_index:
                        middles[c] += 1
                        nms[c] += Hs[c][middles[c]]
                    image_file[i_base][j - base][c] = middles[c]
                else:
                    image_file[i_base][j - base][c] = middles[c]
        i_base = i * 2
        for c in range(channel):
            for a in range(size):
                if image_pad[i_base][j-base+a][c] <= middles[c]:
                    nms[c] -= 1
                Hs[c][image_pad[i_base][j-base+a][c]] -=1
                if image_pad[i_base+size][j-base+a][c] <= middles[c]:
                    nms[c] += 1
                Hs[c][image_pad[i_base+size][j-base+a][c] ] +=1
            if nms[c] > middle_index:
                while nms[c] > middle_index:
                    nms[c] -= Hs[c][middles[c]]
                    middles[c] -= 1
                if nms[c] < middle_index:
                    middles[c] += 1
                    nms[c] += Hs[c][middles[c]]
                image_file[i_base][j - base][c] = middles[c]
            elif nms[c] < middle_index:
                while nms[c] < middle_index:
                    middles[c] += 1
                    nms[c] += Hs[c][middles[c]]
                image_file[i_base][j - base][c] = middles[c]
            else:
                image_file[i_base][j - base][c] = middles[c]
        for j in range(base+1,col+base).__reversed__():
            i_base = i*2+1
            for c in range(channel):
                for a in range(size):
                    if image_pad[i_base+a][j][c]<=middles[c]:
                        nms[c]-=1
                    Hs[c][image_pad[i_base+a][j][c]] -=1
                    if image_pad[i_base+a][j-size][c]<=middles[c]:
                        nms[c]+=1
                    Hs[c][image_pad[i_base+a][j-size][c]] +=1
                if nms[c]> middle_index:
                    while nms[c]>middle_index:
                        nms[c] -= Hs[c][middles[c]]
                        middles[c] -= 1
                    if nms[c] < middle_index:
                        middles[c] += 1
                        nms[c] += Hs[c][middles[c]]
                    image_file[i_base][j-base-1][c] = middles[c]
                elif nms[c] < middle_index:
                    while nms[c] < middle_index:
                        middles[c] += 1
                        nms[c] += Hs[c][middles[c]]
                    image_file[i_base][j - base][c] = middles[c]
                else:
                    image_file[i_base][j - base][c] = middles[c]
    if row%2 == 1 :
        i_base = i * 2 + 2
        for c in range(channel):
            for a in range(size):
                Hs[c][image_pad[i_base - 1][a][c]] -= 1
                Hs[c][image_pad[i_base - 1 + size][a][c]] += 1
                if image_pad[i_base - 1][a][c] <= middles[c]:
                    nms[c] -= 1
                if image_pad[i_base - 1 + size][a][c] <= middles[c]:
                    nms[c] += 1

            if nms[c] > middle_index:
                while nms[c] > middle_index:
                    nms[c] -= Hs[c][middles[c]]
                    middles[c] -= 1
                if nms[c] < middle_index:
                    middles[c] += 1
                    nms[c] += Hs[c][middles[c]]
                image_file[i_base][j - base][c] = middles[c]
            elif nms[c] < middle_index:
                while nms[c] < middle_index:
                    middles[c] += 1
                    nms[c] += Hs[c][middles[c]]
                image_file[i_base][j - base][c] = middles[c]
            else:
                image_file[i_base][j - base][c] = middles[c]

        for j in range(base + 1, col + base):
            i_base = i * 2
            for c in range(channel):
                for a in range(size):
                    if image_pad[i_base + a][j - size][c] <= middles[c]:
                        nms[c] -= 1
                    Hs[c][image_pad[i_base + a][j - size][c]] -=1
                    if image_pad[i_base + a][j][c] <= middles[c]:
                        nms[c] += 1
                    Hs[c][image_pad[i_base + a][j][c]] +=1
                if nms[c] > middle_index:
                    while nms[c] > middle_index:
                        nms[c] -= Hs[c][middles[c]]
                        middles[c] -= 1
                    if nms[c] < middle_index:
                        middles[c] += 1
                        nms[c] += Hs[c][middles[c]]
                    image_file[i_base][j - base][c] = middles[c]
                elif nms[c] < middle_index:
                    while nms[c] < middle_index:
                        middles[c] += 1
                        nms[c] += Hs[c][middles[c]]
                    image_file[i_base][j - base][c] = middles[c]
                else:
                    image_file[i_base][j - base][c] = middles[c]
    return  image_file.astype(np.uint8)

def AverageFilter(image, size=3):
    middle_index = int(size*size/2)+1
    row,col,channel = image.shape
    image_pad = np.zeros((row+size-1,col+size-1,channel),dtype=np.uint8)
    image_file = np.zeros(image.shape)
    image_pad[:image.shape[0],:image.shape[1],:image.shape[2]] = image

    sums=[]
    for c in range(channel):
        sum = 0

        for i in range(size-1):
            for j in range(size):
                sum+=image_pad[i][j][c]
        sums.append(sum)

    base = size-1
    row_num = int(row/2)
    all_num = size*size
    for i in range(row_num):
        i_base = i * 2
        for c in range(channel):
            for a in range(size):
                sums[c]-=image_pad[i_base-1][a][c]
                sums[c]+=image_pad[i_base-1+ size][a][c]
            image_file[i_base][j - base][c] = sums[c]/(all_num)

        for j in range(base+1,col+base):
            i_base = i*2
            for c in range(channel):
                for a in range(size):
                    sums[c] -= image_pad[i_base+a][j-size][c]
                    sums[c] += image_pad[i_base+a][j][c]
                image_file[i_base][j - base][c] = sums[c]/all_num
        i_base = i * 2
        for c in range(channel):
            for a in range(size):
                sums[c] -= image_pad[i_base][j-base+a][c]
                sums[c] +=image_pad[i_base+size][j-base+a][c]
            image_file[i_base][j - base][c] = sums[c]/all_num
        for j in range(base+1,col+base).__reversed__():
            i_base = i*2+1
            for c in range(channel):
                for a in range(size):
                    sums[c] -= image_pad[i_base+a][j][c]
                    sums[c] += image_pad[i_base+a][j-size][c]
                image_file[i_base][j - base][c] = sums[c]/all_num
    if row%2 == 1 :
        i_base = i * 2 + 2
        for c in range(channel):
            for a in range(size):
                sums[c] -= image_pad[i_base - 1][a][c]
                sums[c] += image_pad[i_base - 1 + size][a][c]
            image_file[i_base][j - base][c] = sums[c]/all_num

        for j in range(base + 1, col + base):
            i_base = i * 2
            for c in range(channel):
                for a in range(size):
                    sums[c] -= image_pad[i_base + a][j - size][c]
                    sums[c] += image_pad[i_base + a][j][c]
                image_file[i_base][j - base][c] = sums[c]/all_num

    return  image_file.astype(np.uint8)

def DWT(image):
    channel = image.shape[2]
    i_list = []
    for c in range(channel):
        LL,(LH,HL,HH) = pywt.dwt2(image[:,:,c],"bior1.3")
        row, col = HL.shape
        #thresh = math.sqrt(2 * math.log(row * col, math.e))
        thresh = 10
        for i in range(row):
            for j in range(col):
                    if math.fabs(LH[i][j])<thresh:
                        LH[i][j] = 0
                    if math.fabs(HL[i][j])<thresh:
                        HL[i][j] = 0
                    if math.fabs(HH[i][j])<thresh:
                        HH[i][j] = 0
        re_i = pywt.idwt2((LL,(LH,HL,HH)),"bior1.3")
        re_i = re_i.reshape((re_i.shape[0],re_i.shape[1],1))
        i_list.append(re_i)
    for c in range(1,channel):
        i_list[0]=np.concatenate((i_list[0],i_list[c]),axis=2)
    return i_list[0]

def sobel(image):
    row, col, channel = image.shape
    image_pad = np.zeros((row + 2, col + 2, channel), dtype=np.uint8)
    image_file = np.zeros(image.shape)
    image_soble = np.zeros(image.shape[:2])
    image_pad[:image.shape[0], :image.shape[1], :image.shape[2]] = image
    weight = [-1,-2,-1]
    for i in range(row):
        for j in range(col):
            x = 0
            for c in range(channel):
                h = 0
                v = 0
                for sub in range(3):
                    v += image_pad[i-1+sub][j-1][c]*weight[sub]
                    v -= image_pad[i-1+sub][j+1][c]*weight[sub]
                v/=4
                for sub in range(3):
                    h += image_pad[i-1][j-1+sub][c]*weight[sub]
                    h -= image_pad[i+1][j-1+sub][c]*weight[sub]
                h/=4
                x += math.sqrt(v**2+h**2)
            image_soble[i][j] = x/3
    return image_soble.astype(np.uint8)
def RGB_Y(R,G,B):
    return 0.257*R+0.504*G+0.098*B+16
def threshold(image,thresh):
    gray = RGB_Y(image[:,:,0],image[:,:,1],image[:,:,2])
    row,col = gray.shape
    for i in range(row):
        for j in range(col):
            if gray[i][j]<thresh:
                gray[i][j] = 0
            else:
                gray[i][j] = 255
    return gray

def randomHalfColor(image):
    gray = RGB_Y(image[:,:,0],image[:,:,1],image[:,:,2])
    thresh = np.random.randint(0,255,(gray.shape))
    row, col = gray.shape
    for i in range(row):
        for j in range(col):
            if gray[i][j] < thresh[i][j]:
                gray[i][j] = 0
            else:
                gray[i][j] = 1
    return gray

def PSNR(image):
    y = RGB_Y(image[:,:,0],image[:,:,1],image[:,:,2])
    mean_y = np.mean(y)
    y_2 = np.multiply(y,y)
    mse = np.sum(y_2)/(y.shape[0]*y.shape[1])-mean_y**2
    return 10*math.log((255**2/mse),10)

def SSIM(x,y):
    def calcov(x, y):
        total = 1
        for i in y.shape:
            total = total * i
        mean_y = np.mean(y)
        mean_x = np.mean(x)
        return np.sum(np.multiply(x, y)) / total - mean_y * mean_x
    ux = np.mean(x)
    uy = np.mean(y)

    dxy = calcov(x,y)
    dx = calcov(x,x)
    dy = calcov(y,y)
    c1 = 1
    c2 = 2
    up = (2*ux*uy+c1)*(2*dxy+c2)
    down = (ux**2+uy**2+c1)*(dx+dy+c2)
    return up/down

if __name__ =="__main__":
    L=255
    image=loadpicture("test.jpg")
    imagex=np.array(image)

    row,col=image.shape[:2]
    number = np.linspace(0, L + 1, 256)
    listplt=[311,312,313]
    for c in range(image.shape[2]):
        list = []
        for i in range(L + 1):
            list.append(0)
        for i in range(row):
            for j in range(col):
                list[image[i][j][c]] += 1

        imagetemp=hist_equal(imagex[:,:,c],L)
        imagex[:,:,c]=imagetemp

        listhist = []
        for i in range(L + 1):
            listhist.append(0)
        for i in range(row):
            for j in range(col):
                listhist[imagetemp[i][j]] += 1
        plt.subplot(listplt[c])
        plt.bar(number, np.array(listhist), width=1,facecolor="#9999ff", edgecolor="white")
        plt.bar(number, -np.array(list), width=1,facecolor="#ff9999", edgecolor="white")
        plt.xlim(0, 260)
    plt.show()
    imsave("hist_equal.jpg",imagex)


    Gausssnoise_image = GaussiNois(image,50,50*np.ones(image.shape))
    plt.imshow(Gausssnoise_image)
    plt.show()
    imsave('Gausssnoise_image.jpg',Gausssnoise_image)
    SaltPappernoist_image = SaltPapperNoist(image, 0.1)
    plt.imshow(SaltPappernoist_image)
    plt.show()
    imsave('SaltPappernoist_image.jpg', SaltPappernoist_image)
    print(str(PSNR(image)))
    print("Gaussnoise:" + str(PSNR(Gausssnoise_image)))
    print("SSIM:" + str(SSIM(image, Gausssnoise_image)))
    print("Saltnoise:" + str(PSNR(SaltPappernoist_image)))
    print("SSIM:" + str(SSIM(image, SaltPappernoist_image)))

    G_M_image = middleFilter(Gausssnoise_image)
    print("MGdenoise:"+str(PSNR(G_M_image)))
    print("SSIM:"+str(SSIM(image,G_M_image)))
    plt.imshow(G_M_image)
    plt.show()
    imsave('Gausssnoise_image_after_middleFilter.jpg', G_M_image)
    G_M_image = middleFilter(SaltPappernoist_image)
    print("MSdenoise:"+str(PSNR(G_M_image)))
    print("SSIM:" + str(SSIM(image, G_M_image)))
    plt.imshow(G_M_image)
    plt.show()
    imsave('SaltPappernoist_image_after_middleFilter.jpg', G_M_image)

    G_A_image = AverageFilter(Gausssnoise_image)
    print("AGdenoise:" + str(PSNR(G_A_image)))
    print("SSIM:" + str(SSIM(image, G_A_image)))
    plt.imshow(G_A_image)
    plt.show()
    imsave('Gausssnoise_image_after_AverageFilter.jpg', G_A_image)
    G_A_image = AverageFilter(SaltPappernoist_image)
    print("ASdenoise:" + str(PSNR(G_A_image)))
    print("SSIM:" + str(SSIM(image, G_A_image)))
    plt.imshow(G_A_image)
    plt.show()
    imsave('SaltPappernoist_image_after_AverageFilter.jpg', G_A_image)

    sobelimage = sobel(image)
    plt.imshow(sobelimage)
    plt.show()
    imsave('sobel_image.jpg', sobelimage)

    th_image = threshold(image, 128)
    plt.imshow(th_image,cmap="gray")
    plt.show()
    imsave('threshold_image.jpg', th_image)

    hc_image = randomHalfColor(image)
    plt.imshow(hc_image,cmap="gray")
    plt.show()
    imsave('randomHalfColor_image.jpg', hc_image)

    dwt_image = DWT(Gausssnoise_image)
    plt.imshow(dwt_image)
    plt.show()
    imsave('DWT_image.jpg', dwt_image)