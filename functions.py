import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
import collections
from sklearn import linear_model

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

previous_frames = collections.deque(maxlen=10)

def draw_lines(img, lines, color=[255, 0, 0], thickness=5):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """

    m_tresh_horiz = 0.5
    m_tresh_vert = 0.8

    m_left = []
    x1_left = []
    x2_left = []
    y1_left = []
    y2_left = []

    m_right = []
    x1_right = []
    x2_right = []
    y1_right = []
    y2_right = []

    y_max = img.shape[0]
    y_min = int(img.shape[0]*0.59)

    XLeft = []
    yLeft = []
    XRight = []
    yRight = []

    for line in lines:
        for x1,y1,x2,y2 in line:
            m=(y2-y1)/(x2-x1)
            # remove random horizontal or vertical lines
            if m_tresh_horiz < abs(m) < m_tresh_vert:
                # left line
                if m < 0:
                    m_left.append(m)
                    x1_left.append(x1)
                    x2_left.append(x2)
                    y1_left.append(y1)
                    y2_left.append(y2)
                    XLeft.append(x1)
                    XLeft.append(x2)
                    yLeft.append(y1)
                    yLeft.append(y2)
                # right line
                elif m > 0:
                    m_right.append(m)
                    x1_right.append(x1)
                    x2_right.append(x2)
                    y1_right.append(y1)
                    y2_right.append(y2)
                    XRight.append(x1)
                    XRight.append(x2)
                    yRight.append(y1)
                    yRight.append(y2)

    # left
    m_left_median = np.median(m_left)
    x1_left_median = np.median(x1_left)
    x2_left_median = np.median(x2_left)
    y1_left_median = np.median(y1_left)
    y2_left_median = np.median(y2_left)

    b_left = y1_left_median - m_left_median * x1_left_median

    # right
    m_right_median = np.median(m_right)
    x1_right_median = np.median(x1_right)
    x2_right_median = np.median(x2_right)
    y1_right_median = np.median(y1_right)
    y2_right_median = np.median(y2_right)

    #ransac = linear_model.RANSACRegressor()
    #XLeft = np.array(XLeft)
    #yLeft = np.array(yLeft)
    #ransac.fit(XLeft, yLeft)

    b_right= y1_right_median - m_right_median * x1_right_median

    # Average lines using last 10 frames
    previous_frames.append((m_left_median, b_left, m_right_median, b_right))
    if len(previous_frames) > 0:
        median = np.median(previous_frames, -2)
        m_left = median[0]
        b_left = median[1]
        m_right = median[2]
        b_right = median[3]

    x1_left = int((y_max - b_left) / m_left)
    x2_left = int((y_min - b_left) / m_left)
    x1_right = int((y_max - b_right) / m_right)
    x2_right = int((y_min - b_right) / m_right)

    # Draw left and right line
    cv2.line(img, (x1_left, y_max), (x2_left, y_min), color, thickness)
    cv2.line(img, (x1_right, y_max), (x2_right, y_min), color, thickness)

    #for line in lines:
    #    for x1,y1,x2,y2 in line:
    #        m=(y2-y1)/(x2-x1)
    #        if m_tresh_horiz < abs(m) < m_tresh_vert:
    #            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

    #imshape = img.shape
    #vertices = np.array([[(int(imshape[1]*0.1), imshape[0]),
    #                      (int(imshape[1]*0.425), int(imshape[0]*0.61)),
    #                      (int(imshape[1]*0.595), int(imshape[0]*0.61)),
    #                      (int(imshape[1]*0.97),imshape[0]),
    #                      (int(imshape[1]*0.82), imshape[0]),
    #                      (int(imshape[1]*0.6), int(imshape[0]*0.75)),
    #                      (int(imshape[1]*0.45), int(imshape[0]*0.75)),
    #                      (int(imshape[1]*0.25), imshape[0])]],
    #                      dtype=np.int32)
    #cv2.fillPoly(img, vertices, [0,0,255])

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.
def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)
