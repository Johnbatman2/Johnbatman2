from cmath import rect
from tkinter import CENTER
from typing import List
from unittest import result
import cv2 as cv
from cv2 import threshold
from cv2 import rectangle
from cv2 import MARKER_CROSS
from cv2 import pointPolygonTest
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def findClickPositions(Pmobclose_img_path, Pmob_img_path, threshold=0.04, debug_mode=None):
    Pmob_img = cv.imread(Pmob_img_path, cv.IMREAD_REDUCED_COLOR_2)
    Pmobclose_img = cv.imread(Pmobclose_img_path, cv.IMREAD_REDUCED_COLOR_2)

    Pmobclose_w = Pmobclose_img.shape[1]
    Pmobclose_h = Pmobclose_img.shape[0]

    # found best result in this case
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(Pmob_img, Pmobclose_img, method)

    #something 
    locations = np.where(result >= threshold)
    locations = list(zip(* locations[::-1]))
    #print(locations)

    # need to create a list
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), Pmobclose_w, Pmobclose_h]
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 5)
    #print(rectangle)
    
    points = []
    if len(rectangles):
        print('found Mob')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 0)
        marker_type = cv.MARKER_CROSS 

        # need to loop over all the locations and draw their rectangle
        for (x, y, w, h) in rectangles:

            # derermine the boc positions
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # save the points 
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # determine the box positions
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # draw the box
                cv.rectangle(Pmob_img, top_left, bottom_right, line_color, line_type)
            elif debug_mode == 'points':
                cv.drawMarker(Pmob_img, (center_x, center_y), marker_color, marker_type)

        if debug_mode:
            cv.imshow('matches', Pmob_img)
            cv.waitKey()
            #cv.imwrite('result.png', Pmob_img)

    return points


points = findClickPositions('Pmob_img', 'Pmobclose_img', debug_mode='points')
print(points)

# code is not runing because it cant find the images in our directory