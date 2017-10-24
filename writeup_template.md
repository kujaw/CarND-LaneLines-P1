# **Finding Lane Lines on the Road** 


The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the _lines() function.

My pipeline consisted of 6 steps. First, I convert the image to grayscale (img 1), then I blurr it using Gaussian blurr filter to reduce image noise (img 2). Those two steps are necessary to further perform edge detection on the image using Canny edge detection algorithm (img 3). Afterwards I draft area of interest for line finding algorithm so that no lines will be detected outside this area making whole process more accurate (img 4). Then the image is processed by Hough Line Transform to output detected straight lines on black blackground (img 6). The last, sixth step, is to combine original image and image with only drawn lines so user can see original image with lineson it (img 7).

In order to draw a single line on the left and right side of a lane, I modified the draw_lines() function by splitting lines for left and right lane using computed slopes of those lines. Then for each lane, for each slope and point I computed median so that I've got only one averaged slope and two averaged points for each line. In order to get more stability I've used moving average (median) over 10 last frames. In the end, I've got two averaged lines which I draw using cv2.lines() function. Compare img 5 and img 6 for difference between before/after modification.

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming is that lines are not stable enough. That's probably caused by treshold values used to compute Canny edge algorithm. There are too many random edges which are later recognized as lines. The soulution would be to raise tresholds of Canny edge detection to get rid of some random edges. There will be some frames where lines are not recognized - in that case I could draw lines using previously saved averaged values.


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to use some more reliable smoothing algorithm, like RANSAC.
