#coding:utf-8


#coding:utf-8


from MsgClient import MsClient
from config import *

END_STRING = "finish"
import json
from duojidd import duojidd
def processMessage(message):
    if message['from'] =='AngleCaculator' and message['type']=='SETANGLE':

        degreeInfo = None
        try:
            degreeInfo = message['data']
        except Exception as e:
            print(e)
        degreeX = degreeInfo['degreeX']
        degreeZ = degreeInfo['degreeZ']
        duojidd(degreeX,degreeZ)


if __name__ == '__main__':

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)

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
            processMessage(message)