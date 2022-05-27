from re import X
from tkinter import W, Y
import cv2 as cv
from cv2 import threshold
from cv2 import rectangle
from cv2 import rectify3Collinear
import numpy as np
import os



os.chdir(os.path.dirname(os.path.abspath(__file__)))

def findClickPositions(close_img_path, whole_img_path, threshold= 0.98, debug_mode=None):

    whole_img = cv.imread(whole_img_path, cv.IMREAD_REDUCED_COLOR_2)
    close_img = cv.imread(close_img_path, cv.IMREAD_REDUCED_COLOR_2)

    close_w = close_img.shape[1]
    close_h = close_img.shape[0]

    method = cv.TM_CCORR_NORMED
    result = cv.matchTemplate(whole_img, close_img, method)


    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    print(locations)

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), close_w, close_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 2)
    print(rectangles)

    points = []
    if len(rectangles):
        print('Found mob.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 0)
        marker_Type = cv.MARKER_CROSS

        
        # Loop over all the locations and draw their rectangle
        for (x, y, w, h) in rectangles:

            center_x = x + int(h/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                top_left = (x, y)
                bottom_right = (x + w, y + h)

                cv.rectangle(whole_img, top_left, bottom_right, line_color, line_type )
            elif debug_mode == 'points':
                cv.drawMarker(whole_img, (center_x, center_y), marker_color, marker_Type)
            
        if debug_mode:
            cv.imshow('matches', whole_img)
            cv.waitKey()
        
    return points 

points = findClickPositions('close.png', 'whole.png', debug_mode='points')
print(points)

     
