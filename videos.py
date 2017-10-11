import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
from functions import *
from moviepy.editor import VideoFileClip
from IPython.display import HTML

def process_image(image):
    
    image = mpimg.imread(image)
    # Read in and grayscale the image
    gray = grayscale(image)

    # Define a kernel size and apply Gaussian smoothing
    kernel_size = 7
    blur_gray = gaussian_blur(gray, kernel_size)

    # Define our parameters for Canny and apply
    low_threshold = 2
    high_threshold = 100
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
    threshold = 14   # minimum number of votes (intersections in Hough grid cell)
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

    return color_edges 

#white_output = 'test_videos_output/solidWhiteRight.mp4'
#clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
#white_clip = clip1.fl_image(process_image)
#
#white_clip.write_videofile(white_output, audio=False)
#
#clip1.reader.close()
#clip1.audio.reader.close_proc()

#yellow_output = 'test_videos_output/solidYellowLeft.mp4'
#clip2 = VideoFileClip('test_videos/solidYellowLeft.mp4')#.subclip(15,)
#yellow_clip = clip2.fl_image(process_image)
#
#
#yellow_clip.write_videofile(yellow_output, audio=False)
#
#clip2.reader.close()
#clip2.audio.reader.close_proc()

challenge_output = 'test_videos_output/challenge.mp4'
clip3 = VideoFileClip('test_videos/challenge.mp4').subclip(3,)
challenge_clip = clip3.fl_image(process_image)

# create images of frames for easier debugging
challenge_clip.write_images_sequence("test_videos_frames/frame%03da.jpg")

#challenge_clip.write_videofile(challenge_output, audio=False)

clip3.reader.close()
clip3.audio.reader.close_proc()
