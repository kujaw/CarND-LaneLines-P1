import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
from imagefunctions import *

# Read in and grayscale the image
for filename in os.listdir('test_videos_frames'):
    image = mpimg.imread('test_videos_frames/{}'.format(filename))

    gray = grayscale(image)

    # Define a kernel size and apply Gaussian smoothing
    kernel_size = 5
    blur_gray = gaussian_blur(gray, kernel_size)

    # Define our parameters for Canny and apply
    low_threshold = 60
    high_threshold = 180
    edges = canny(blur_gray, low_threshold, high_threshold)

    # Define region of interest
    imshape = image.shape
    vertices = np.array([[(0,imshape[0]),(450, 320), (490, 320), (imshape[1],imshape[0])]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)

    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 2 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 10    # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 15 #minimum number of pixels making up a line
    max_line_gap = 15    # maximum gap in pixels between connectable line segments
    line_image = np.copy(image)*0 # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    #lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
    #                            min_line_length, max_line_gap)
    lines = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

    # Create a "color" binary image to combine with line image
    color_edges = np.dstack((edges, edges, edges))

    # Draw the lines on the edge image
    #lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)
    lines_edges = weighted_img(lines, image, α=0.8, β=1., λ=0.)

    #plt.imshow(lines_edges)
    plt.imshow(masked_edges)
    plt.title('{}'.format(filename))
    plt.show()
