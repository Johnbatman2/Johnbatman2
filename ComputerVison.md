import cv2 as cv
import os
from time import time
from eyes import WindowCapture

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class

wincap = WindowCapture('your Application')
WindowCapture.list_window_names('self')

loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
