import numpy as np
import matplotlib.pyplot as plt
from skimage import filters


def entropy_1D(hist, threshold):
    foreground = hist[:threshold]
    background = hist[threshold:]

    foreground_prob = foreground / (sum(foreground) + np.finfo(float).eps)
    background_prob = background / (sum(background) + np.finfo(float).eps)

    foreground_entropy = -np.sum(foreground_prob * np.log2(foreground_prob + np.finfo(float).eps))
    background_entropy = -np.sum(background_prob * np.log2(background_prob + np.finfo(float).eps))

    total_entropy = foreground_entropy + background_entropy
    return total_entropy

def max_entropy_1D(hist):
    max_ent, threshold = 0, 0
    for t in range(len(hist)):
        total_entropy = entropy_1D(hist,t)
        if total_entropy > max_ent:
            max_ent = total_entropy
            threshold = t
    return threshold

def plot_entropy_1D(hist):
    # Calculate entropies for all possible thresholds
    thresholds = np.arange(len(hist))
    entropies = [entropy_1D(hist, t) for t in thresholds]

    # Plot entropy curve
    plt.plot(thresholds, entropies)
    plt.title("Entropy 1D Curve")
    plt.xlabel("Threshold")
    plt.ylabel("Entropy")
    plt.savefig('1D_Entropy_Curve.jpg')
    plt.show()

def algo_1D(gray_image):
    # Calculate 1D histogram
    hist, bins = np.histogram(gray_image.ravel(), 256, [0, 255])

    # Plot 1D histogram
    plt.plot(hist)
    plt.title("1D Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    plt.savefig('1D_Histogram.jpg')
    plt.show()

    # Calculate and apply 1D max-entropy threshold
    threshold_1D = max_entropy_1D(hist)
    plot_entropy_1D(hist)
    print(threshold_1D)
    binary_image = gray_image > threshold_1D
    # Plot binary image with 1D max-entropy threshold
    plt.imshow(binary_image, cmap='gray')
    plt.title("1D Max-Entropy Threshold")
    plt.savefig('1D_Max_Entropy_Threshold.jpg')
    plt.show()

def entropy_2D(hist_2d, threshold_x):
    foreground = hist_2d[:threshold_x, :]
    background = hist_2d[threshold_x:, :]

    foreground_prob = foreground / (np.sum(foreground) + np.finfo(float).eps)
    background_prob = background / (np.sum(background) + np.finfo(float).eps)

    foreground_entropy = -np.sum(foreground_prob * np.log2(foreground_prob + np.finfo(float).eps))
    background_entropy = -np.sum(background_prob * np.log2(background_prob + np.finfo(float).eps))

    total_entropy = foreground_entropy + background_entropy
    return total_entropy

def max_entropy_2D(hist_2d):
    max_ent, threshold = 0, 0
    for t in range(hist_2d.shape[0]):
        total_entropy = entropy_2D(hist_2d,t)
        if total_entropy > max_ent:
            max_ent = total_entropy
            threshold = t
    return threshold


def plot_entropy_2D(hist_2d):
    # Calculate entropies for all possible thresholds
    thresholds = np.arange(len(hist_2d[0]))
    entropies = [entropy_2D(hist_2d, t) for t in thresholds]

    # Plot entropy curve
    plt.plot(thresholds, entropies)
    plt.title("Entropy 2D Curve")
    plt.xlabel("Threshold")
    plt.ylabel("Entropy")
    plt.savefig('2D_Entropy_Curve.jpg')
    plt.show()



def algo_2D(gray_image):
    # 基于图像像素值和邻域平均值的二维最大熵阈值分割
    # Calculate neighborhood average for each pixel
    neighborhood_average = filters.rank.mean(gray_image, np.ones((3, 3)))

    # Create 2D histogram using pixel values and neighborhood averages
    hist_2d, x_edges, y_edges = np.histogram2d(gray_image.ravel(), neighborhood_average.ravel(), bins=256)

    # Plot 2D histogram
    plt.imshow(hist_2d.T, origin='lower', cmap='hot', aspect='auto')
    plt.colorbar(label='Frequency')
    plt.xlabel('Pixel Value')
    plt.ylabel('Neighborhood Average')
    plt.title('2D Histogram')
    plt.savefig('2D_Histogram.jpg')
    plt.show()

    # Calculate and apply 2D max-entropy threshold
    threshold_2D = max_entropy_2D(hist_2d)
    plot_entropy_2D(hist_2d)
    print(threshold_2D)
    binary_image_2D = gray_image > threshold_2D

    # Plot binary image with 2D max-entropy threshold
    plt.imshow(binary_image_2D, cmap='gray')
    plt.title("2D Max-Entropy Threshold Based on Pixel Value and Neighborhood")
    plt.savefig('2D_Max_Entropy_Threshold.jpg')
    plt.show()

    # 基于梯度幅值和方向的二维最大熵阈值分割
    # # Calculate gradient magnitude and direction
    # sobel_x = filters.sobel_h(gray_image)
    # sobel_y = filters.sobel_v(gray_image)
    # gradient_magnitude = np.hypot(sobel_x, sobel_y)
    # gradient_direction = np.arctan2(sobel_y, sobel_x)
    #
    # # Calculate 2D histogram
    # hist_2d, x_edges, y_edges = np.histogram2d(gradient_magnitude.ravel(), gradient_direction.ravel(), bins=64)
    #
    # # Plot 2D histogram
    # plt.imshow(hist_2d.T, origin='lower', cmap='hot', aspect='auto')
    # plt.colorbar(label='Frequency')
    # plt.xlabel('Gradient Magnitude')
    # plt.ylabel('Gradient Direction')
    # plt.title('2D Histogram')
    # plt.show()
    #
    # # Calculate and apply 2D max-entropy threshold
    # threshold_2D = max_entropy_2D(hist_2d)
    # binary_image_2D = gradient_magnitude > threshold_2D
    #
    # # Plot binary image with 2D max-entropy threshold
    # plt.imshow(binary_image_2D, cmap='gray')
    # plt.title("2D Max-Entropy Threshold")
    # plt.show()