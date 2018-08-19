#coding:utf-8


from MsgClient import MsClient
from config import *

from FaceDector import FaceDetector
import cv2
from tools import buildMsg
END_STRING = "finish"
import json

def processMessage(message,faceDetector,client,subscription):

    if message['type'] in ('FACEDETECT',):
        result = faceDetector.faceDect()
        print(result)
        resultMessage = buildMsg(result)
        client.senMsg(subscription,resultMessage)


if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)

    faceDetector = FaceDetector()

    while True:
        for item in client.pubsub.listen():
            if item['type'] in ("subscribe", "unsubscribe"):
                continue
            if str(item['data'], 'utf-8') in (END_STRING,):
                client.pubsub.unsubscribe()
                break
            message = item['data']
            try:
                message = json.loads(message)
            except Exception as e :
                print(e)
                continue
            processMessage(message,faceDetector,client,subscription)