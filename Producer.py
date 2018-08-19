#coding:utf-8


from MsgClient import MsClient
from config import *
import sys
sys.path.append("/home/pi/SungemSDK/api/")

from FaceDector import FaceDetector
import cv2
from tools import buildMsg
import time

if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)
    #client.start()

    faceDetector = FaceDetector()

    while True:

        result = faceDetector.faceDect()
        image = result[0]
        bbs = result[1]
        key = time.sleep(3)

        boundingBoxes = []
        for i in bbs:
            print(i)
            i[1] = str(i[1])
            boundingBoxes.append(i)

        imageInfo = {}
        imageInfo['imageShape'] = image.shape
        if len(boundingBoxes)==0:
            boundingBoxes = [[]]

        imageInfo['bbs'] = boundingBoxes
        faceMsg = buildMsg(imageInfo)
        client.senMsg(subscription,faceMsg)

        # get face objector
        # if len(bbs) > 0:
        #     box = bbs[0]
        #
        #
        #     if ((box[5] - box[3]) > 10) and ((box[4] - box[2]) > 10):
        #         faceMsg = buildMsg(imageInfo)
        #         client.senMsg(subscription, faceMsg)
