#! /usr/bin/env python3
#coding:utf-8

'''author:liuhj'''

import numpy as np,cv2,sys
sys.path.append("/home/pi/SungemSDK/api/")
import hsapi as hs

WEBCAM = False
class FaceDetector():
    def __init__(self):
       self.net = hs.HS('FaceDetector',zoom=True,verbose=2,threshSSD=0.55)
    #net = hs.HS('FaceDetetor',zoom = True,verbose = 2, threshSSD=0.55)
        #pass


    def faceDect(self):
        img = None
        result =self.net.run(img)
        return result


if __name__ == '__main__':
    pass



