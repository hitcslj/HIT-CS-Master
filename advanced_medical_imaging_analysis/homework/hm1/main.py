from skimage import io
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte
from utils import algo_1D,algo_2D
import argparse

parser = argparse.ArgumentParser(description='最大熵阈值分割算法')
parser.add_argument('--algo',
                    type=str,
                    default='1d',
                    help='algorithm name: 1d, 2d')
args = parser.parse_args()

if __name__ == '__main__':
    # Load image and convert to grayscale
    image_path = 'test.png'
    image = io.imread(image_path)
    gray_image = img_as_ubyte(rgb2gray(image))
    if args.algo=='1d':
        algo_1D(gray_image)
    elif args.algo=='2d':
        algo_2D(gray_image)
    else:
        raise ValueError




