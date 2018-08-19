#coding:utf-8


from MsgClient import MsClient
from config import *

import cv2
from tools import buildMsg,buildMotorMsg
import math

import json
import datetime


END_STRING = "finish"

import time

hasPerson = False



DEGREEX = 0
DEGREEZ = 0


startDegreeX = -30
startDegreeZ = -15

count = 0

IMAGEWIDTH = 1800
IMAGEHEIGTH = 1600

CARWIDTH = 180

MAXCOUNT = 5

PERX = 0
PERY = 0
PERZ = 0

BESTGET = False


def isFace(faceInfo):
    if len(faceInfo[0]) > 0:
        box = faceInfo[0]
        score = float(box[1])
        if box[5] - box[3] > 10 or box[4] - box[2] > 10 and score > 0.55:
            return True

    return False

def getXangle(imageLocation,widthSize,angle):

    score = float(imageLocation[1])
    x1 = imageLocation[2]
    y1 = imageLocation[3]
    x2 = imageLocation[4]
    y2 = imageLocation[5]
    if score > 0.55:
        xMiddle = (x1+x2)/2
        if xMiddle>(widthSize/2-50) and xMiddle<(widthSize/2+50):
            return angle

    return None


def getYangle(imageLocation, heightSize, angle):
    score = float(imageLocation[1])
    x1 = imageLocation[2]
    y1 = imageLocation[3]
    x2 = imageLocation[4]
    y2 = imageLocation[5]
    if score > 0.55:
        yMiddle = (y1 + y2) / 2
        if yMiddle > (heightSize / 2 - 20) and yMiddle < (heightSize / 2 + 20):
            return angle

    return None

def getPosition(xAngle,yAngle,carWidth):
    assert(xAngle>-90 and xAngle<90)
    assert (yAngle>-90 and yAngle<90)
    x = float(carWidth)/4
    y = (float(carWidth)/4)/math.tan(abs(xAngle))
    z = y*math.tan(abs(yAngle))
    return (x,y,z)


def getBestAngle(x,y,z):

    xAngle = -10
    yAngle = -5
    return (xAngle,yAngle)

def processMessage(message,client,subscription):
    global DEGREEX
    global DEGREEZ
    global hasPerson
    global  count
    global  BESTGET
    global LastestTimeHasPerson

    #步进 度数
    step = 2

    if message['from'] in ('VIDEO',):
        if message['type'] in ('VIDEOINFO',):
            faceInfoes = message['data']
            imageShape = faceInfoes['imageShape']
            print(imageShape)
            IMAGEWIDTH = imageShape[1]
            IMAGEHEIGTH = imageShape[0]
            faceInfo = faceInfoes['bbs']


            #检测到有人
            if isFace(faceInfo):
                print("......检测到人......")
                print(count)
                LastestTimeHasPerson = datetime.datetime.now()

                if BESTGET:
                    return

                if not hasPerson and (count < MAXCOUNT):
                    count =count+1

                #检测到有人进来 开始计算 最佳位置
                if not hasPerson and (count>= MAXCOUNT):
                    print("....监测到人进入....")
                    hasPerson = True
                    #移动到初始位置
                    # xAdd = XANGLE - startXAngle
                    # yAdd = YANGLE - startYAngle
                    DEGREEX = startDegreeX
                    DEGREEZ = startDegreeZ



                    motorAngle = {
                        'degreeX': DEGREEX,
                        'degreeZ': DEGREEZ
                    }
                    msg = buildMotorMsg(motorAngle)
                    print("....发送消息给舵机到初始位置...")
                    print(msg)

                    client.senMsg(subscription,msg)
                    time.sleep(1)

                if hasPerson:

                    xAngle = getXangle(faceInfo[0],IMAGEWIDTH,DEGREEX)
                    if not xAngle:

                        xAdd = step
                        DEGREEX = DEGREEX + xAdd
                        yAdd = 0
                        DEGREEZ = DEGREEZ+yAdd
                        motorAngle = {
                            'degreeX': DEGREEX,
                            'degreeZ': DEGREEZ
                        }
                        msg = buildMotorMsg(motorAngle)
                        print("....发送消息给舵机增加x角度....")
                        print(msg)
                        client.senMsg(subscription, msg)
                        time.sleep(1)

                    yAngle = getYangle(faceInfo[0],IMAGEHEIGTH,DEGREEZ)
                    if not yAngle and xAngle:

                        xAdd = 0
                        DEGREEX = DEGREEZ + xAdd
                        yAdd = step
                        DEGREEZ = DEGREEZ + yAdd

                        motorAngle = {
                            'degreeX': DEGREEX,
                            'degreeZ': DEGREEZ
                        }
                        msg = buildMotorMsg(motorAngle)
                        print("....发送消息给舵机增加y角度....")
                        print(msg)
                        client.senMsg(subscription, msg)
                        time.sleep(1)
                    if xAngle and yAngle:
                        print("....xy角度获得....")
                        print(xAngle)
                        print(yAngle)

                        x,y,z = getPosition(xAngle,yAngle,CARWIDTH)
                        print("....坐标位置获得....")
                        print(x,y,z)
                        bestXangle,bestYangle = getBestAngle(x,y,z)
                        print("....角度获得....")
                        print(bestXangle)
                        print(bestYangle)

                        DEGREEX = bestXangle
                        DEGREEZ = bestYangle

                        motorAngle = {
                            'degreeX': DEGREEX,
                            'degreeZ': DEGREEZ
                        }
                        msg = buildMotorMsg(motorAngle)
                        print("....发送消息给舵机旋转角度....")
                        print(msg)
                        client.senMsg(subscription, msg)
                        BESTGET = True
                        time.sleep(1)


            else:
                # 没有人

                if hasPerson and count>0:
                    count=count-1
                    time.sleep(1)
                else:
                    count = 0
                    hasPerson = False
                    BESTGET = False
                    time.sleep(1)



if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)

    while True:
        now = datetime.datetime.now()
        for item in client.pubsub.listen():
            if item['type'] in ("subscribe", "unsubscribe"):
                continue
            if str(item['data'], 'utf-8') in (END_STRING,):
                client.pubsub.unsubscribe()
                break
            message = item['data']
            #print(message)
            message = json.loads(message)

            processMessage(message,client,subscription)
            print(DEGREEX,DEGREEZ)

