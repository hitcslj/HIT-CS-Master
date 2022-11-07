# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import math
import time
import PIL.Image
import cv2
import matplotlib.pyplot as plt
from imageio import imsave

def RGB_Y(R,G,B):
    return 0.257*R+0.504*G+0.098*B+16

def Histenequ(image,L):
    row=image.shape[0]
    col=image.shape[1]
    total=row*col
    diclist=[]
    imagetemp=np.array(image)
    imagec=np.array(image)
    dict={}
    list=[]
    for i in range(L+1):
        list.append(0)
    for i in range(row):
        for j in range(col):
            list[imagec[i][j]]+=1
    indexpre=0
    for i in range(L+1):
        if list[i]!=0:
            break
        indexpre+=1
    indexlast=L
    for i in range(L+1):
        if list[L-i]!=0:
            break
        indexlast-=1
    num=indexlast-indexpre+1
    pre=0
    for i in range(num):
        index=indexpre+i
        temp=((pre*total/(float(L)))+list[index])*L/(float(total))
        pre=temp
        dict[index]=temp
    diclist.append(dict)
    for i in range(row):
        for j in range(col):
            imagetemp[i][j]=np.uint8(dict[imagetemp[i][j]]+0.5)
    return imagetemp,diclist
def FTTtwodim(picture):
    row=picture.shape[0]
    col=picture.shape[1]
    dictFTT={}
    dictfinal={}
    for x in range(row):
        dictF=FTTonedim(picture[x,:])
        for v in dictF.keys():
            dictFTT[(x,v)]=dictF[v]
    pxtemp=np.array(picture,dtype=np.complex)
    for v in range(col):
        for x in range(row):
            pxtemp[x][v]=dictFTT[(x,v)]
        dictF=FTTonedim(pxtemp[:,v])
        for u in range(row):
            dictfinal[(u,v)]=dictF[u]
    return dictfinal
def FTTonedim(data):
    dictF={}
    number=data.size
    if number==1:
        dictF[0]=data[0]
        return dictF
    nx=int(number/2)
    datatemp=tranlatepic(data)
    dicteven=FTTonedim(datatemp[:nx])
    dictodd=FTTonedim(datatemp[nx:])
    for u in range(nx):
        w=Wuk(number,u)
        dictF[u]=(dicteven[u]+dictodd[u]*w)/2
        dictF[u+nx]=(dicteven[u]-dictodd[u]*w)/2
    return dictF
def tranlatepic(image):
    col=image.size
    coltemp=int(col/2)
    imagetemp=np.array(image)
    imagex=np.array(image)
    for y in range(coltemp):
       imagetemp[y]=image[y*2]
       imagex[y]=image[2*y+1]
    imagetemp[coltemp:]=imagex[:coltemp]
    return imagetemp
def Wuk(k,u):
    return (complex(math.cos(2*math.pi*u/k),-math.sin(2*math.pi*u/k)))

def FTTforimage(imagex,channel):
    image=cv2.imread(imagex,cv2.IMREAD_GRAYSCALE)
    size=512
    numberrow=int(image.shape[0]/size)
    numbercol=int(image.shape[1]/size)
    imageimage = np.zeros((size, size))
    if channel!=1:
        imageFFT = np.zeros((size, size,channel))
        for c in range(channel):
            for x in range(numberrow):
                for y in range(numbercol):
                    imagetemp=np.array(image[x*size:x*size+size,y*size:y*size+size,c])
                    for u in range(size):
                        for v in range(size):
                            imagetemp[u][v]*=math.pow(-1,u+v)
                    dictF=FTTtwodim(imagetemp)
                    for u in range(size):
                        for v in range(size):
                            imageFFT[u][v][c]+=dictF[(u,v)].real
    else:
        imageimage = np.zeros((size, size))
        imageFFT=np.zeros((size,size),dtype=np.complex)
        for x in range(numberrow):
            for y in range(numbercol):
                imagetemp = np.array(image[x* size:x * size + size, y * size:y * size + size])
                for u in range(size):
                    for v in range(size):
                        imagetemp[u][v] *= math.pow(-1, u + v)
                dictF = FTTtwodim(imagetemp)
                for u in range(size):
                    for v in range(size):
                        imageimage[u][v]=math.sqrt((dictF[(u,v)].real)**2+(dictF[(u,v)].imag)**2)
                        imageFFT[u][v]=dictF[(u,v)]
        imageFFT[0][0]=0
        imageimage=np.array(imageimage)
        imageimage[0][0]=0
        max = np.max(imageimage)
        min = np.min(imageimage)
        temp=(imageimage - min) * 255 / (max - min)
        imageimage = np.array(temp, dtype=np.uint8)
        imageimage,xx=Histenequ(imageimage,255)
    return imageimage,imageFFT

def IDFFT(picture):
    preal = np.array(picture.real)
    picture -= preal
    picture = -picture
    picture += preal

    dictf=FTTtwodim(picture)

    row=picture.shape[0]
    col=picture.shape[1]
    for u in range(row):
        for v in range(col):
            picture[u][v]=dictf[(u,v)]
    picture/=(row*col)
    preal = np.array(picture.real)
    picture=picture-preal
    picture=-picture
    picture=picture+preal
    for u in range(row):
        for v in range(col):
            picture[u][v]*=math.pow(-1,u+v)
    return picture.real

def DCT(image):
    def c(x):
        if x==0:
            return math.sqrt(1/8)
        else:
            return 1/2

    def dct(image,x,y):
        result = 0
        cx = c(x)
        cy = c(y)
        for i in range(8):
            for j in range(8):
                result += cx*cy*image[i][j]*math.cos(math.pi*(i+0.5)*x/8)*math.cos(math.pi*(j+0.5)*y/8)
        return result

    row,col =image.shape

    row_a = (int((row-1)/8))+1
    col_a = (int((col-1)/8))+1
    image_a = np.zeros((row_a*8,col_a*8))

    DFT_image = np.zeros(image_a.shape)

    image_a[:row,:col] = image


    for r_b in range(row_a):
        for c_b in range(col_a):
            r_base = r_b*8
            c_base = c_b*8
            for x in range(8):
                for y in range(8):
                    result = dct(image_a[r_base:(r_base+8),c_base:(c_base+8)],x,y)
                    DFT_image[r_base+x,c_base+y] = result

    return DFT_image

def IDCT(image):
    def c(x):
        if x==0:
            return math.sqrt(1/8)
        else:
            return 1/2

    def dct(image,x,y):
        result = 0
        for i in range(8):
            for j in range(8):
                result += c(i)*c(j)*image[i][j]*math.cos(math.pi*(x+0.5)*i/8)*math.cos(math.pi*(y+0.5)*j/8)
        return result

    row,col =image.shape

    row_a = (int((row-1)/8))+1
    col_a = (int((col-1)/8))+1
    image_a = np.zeros((row_a*8,col_a*8))

    DFT_image = np.zeros(image_a.shape)

    image_a[:row,:col] = image


    for r_b in range(row_a):
        for c_b in range(col_a):
            r_base = r_b*8
            c_base = c_b*8
            for x in range(8):
                for y in range(8):
                    result = dct(image_a[r_base:(r_base+8),c_base:(c_base+8)],x,y)
                    DFT_image[r_base+x,c_base+y] = result

    return DFT_image
def zig_zag(image,lamda):
    row,col =image.shape

    row_a = int((row)/8)
    col_a = int((col)/8)

    zig_image = np.zeros(image.shape)
    for r_b in range(row_a):
        for c_b in range(col_a):
            r_base = r_b*8
            c_base = c_b*8
            i_index = 0
            j_index = 0
            r_add = -1
            c_add = 1
            for i in range(lamda):
                zig_image[r_base+i_index][c_base+j_index] = image[r_base+i_index][c_base+j_index]
                if (i_index+r_add)<0:
                    if (j_index+1)<8:
                        r_add *= -1
                        c_add *= -1
                        j_index+=1
                    else:
                        r_add *= -1
                        c_add *= -1
                        i_index += 1
                elif (j_index+c_add)<0:
                    if (i_index+1)<8:
                        r_add *= -1
                        c_add *= -1
                        i_index+=1
                    else:
                        r_add *= -1
                        c_add *= -1
                        j_index += 1
                else:
                    i_index+=r_add
                    j_index+=c_add
    return zig_image

def PSNR(x,y):
    s = np.subtract(x,y)
    mse = np.multiply(s,s).mean()
    return 10*math.log((np.max(x))**2/mse,10)
if __name__ == '__main__':

    image = PIL.Image.open("test.png")
    image = np.array(image)
    Y = RGB_Y(image[:, :, 0], image[:, :, 1], image[:, :, 2])

    #DFT
    begin = time.time()
    image,DFTimage= FTTforimage("test.png",channel=1)
    end = time.time()
    print(end-begin)
    plt.imshow(image, cmap="gray")
    plt.show()
    image = np.array(image)
    image = PIL.Image.fromarray(image)
    image.convert("L")
    image.save("DFT_test.png")


    IDFTimage = IDFFT(DFTimage)
    plt.imshow(IDFTimage, cmap="gray")
    plt.show()
    imsave("IDFFT_test.png", IDFTimage)

    #fu zhi iDFT
    amp = np.sqrt(np.multiply(DFTimage.imag*10,DFTimage.imag*10)+np.multiply(DFTimage.real*10,DFTimage.real*10))/10

    amp = amp.astype(np.complex_)
    IDFTimage= IDFFT(amp)

    plt.imshow(IDFTimage, cmap="gray")
    plt.show()
    IDFTimage_save = ((
            IDFTimage - np.min(IDFTimage) )* 256.0 / (np.max(IDFTimage) - np.min(IDFTimage))).astype(
        np.uint8)
    (PIL.Image.fromarray(IDFTimage_save, "L")).save("amp_IDFT_test.png")



    #ping lv iDFT
    alpha = np.arctan(DFTimage.imag, DFTimage.real)
    temp = alpha.astype(np.complex_)
    temp.real = np.cos(alpha)
    temp.imag = -np.sin(alpha)
    alpha = temp
    aDDFTi = IDFFT(alpha)
    aDDFTi[0][0] = 0
    aDDFTi_save = ((
            aDDFTi - np.min(aDDFTi)) * 256/ (np.max(aDDFTi) - np.min(aDDFTi))).astype(
        np.uint8)
    (PIL.Image.fromarray(aDDFTi_save, "L")).save("alpha_IDFT_test.png")

    #DCT
    DCTimage = DCT(Y)
    DCTimage_save = (
                DCTimage - np.min(DCTimage) * 256 / (np.max(DCTimage) - np.min(DCTimage))).astype(
        np.uint8)
    (PIL.Image.fromarray(DCTimage_save, "L")).save("DCT_test.png")

    zig_image = zig_zag(DCTimage, 10)
    zig_image = IDCT(zig_image)
    zig_image = (
            zig_image - np.min(zig_image) * 256 / (np.max(zig_image) - np.min(zig_image))).astype(
        np.uint8)
    (PIL.Image.fromarray(zig_image, "L")).save("IDCT_test.png")
    
    lamdas = [1,2,4,6,8,10]
    for lamda in lamdas:
        zig_image = zig_zag(DCTimage,lamda)
        zig_image = IDCT(zig_image)
        zig_image = (
                zig_image - np.min(zig_image) * 256 / (np.max(zig_image) - np.min(zig_image))).astype(
            np.uint8)

        psnr = PSNR(Y, zig_image)
        print(str(lamda)+" : "+str(psnr))

