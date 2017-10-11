import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
from functions import *

# Read in and grayscale the image
for filename in os.listdir('test_images'):
    image = mpimg.imread('test_images/{}'.format(filename))

    gray = grayscale(image)

    # Define a kernel size and apply Gaussian smoothing
    kernel_size = 7
    blur_gray = gaussian_blur(gray, kernel_size)

    # Define our parameters for Canny and apply
    low_threshold = 20
    high_threshold = 80
    edges = canny(blur_gray, low_threshold, high_threshold)

    # Define region of interest
    imshape = image.shape
    vertices = np.array([[(int(imshape[1]*0.1),imshape[0]),
                          (int(imshape[1])*0.425, int(imshape[0]*0.61)),
                          (int(imshape[1])*0.575, int(imshape[0]*0.61)), 
                          (int(imshape[1]*0.95),imshape[0])]], dtype=np.int32)
    masked_edges = region_of_interest(edges, vertices)

    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 1 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 14    # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 25 #minimum number of pixels making up a line
    max_line_gap = 10    # maximum gap in pixels between connectable line segments
    line_image = np.copy(image)*0 # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

    # Create a "color" binary image to combine with line image
    color_edges = np.dstack((edges, edges, edges))

    # Draw the lines on the edge image
    lines_edges = weighted_img(lines, image, α=0.8, β=1., λ=0.)

    ## Show image
    #plt.imshow(lines_edges)
    #plt.title('{}'.format(filename))
    #plt.show()
    
    ## Write image
    cv2.imwrite("test_images/aa{}".format(filename), cv2.cvtColor(lines_edges, cv2.COLOR_RGB2BGR))
