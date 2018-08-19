#coding:utf-8

import redis
import threading


from config import *


class MsClient():
    """ Creates the Redis Client and subscribes to the initial channel """

    def __init__(self, channels, redisServer):

        self.redisServer = redisServer
        self.redis = redis.Redis(host=self.redisServer, port=6379)
        self.pubsub = self.redis.pubsub()
        self.channels = channels
        self.pubsub.subscribe(self.channels)

    def subscribe(self, channels):
        """ The main thread prompts to subscribe to a new channels
            so this function allow the main thread to change the subscription
        """
        self.pubsub.unsubscribe(self.channels)
        self.channels = channels
        self.pubsub.subscribe(channels)

    def senMsg(self, channel, msg):
        self.redis.publish(channel=channel, message=msg)




if __name__ == "__main__":

    redisServer, subscription, port = parameter()

    client = MsClient([subscription, ], redisServer)

    lastSubscription = subscription
    END_STRING ='stop'

    while True:
        command = input("enter 'publish' or a channel ('{0}' to quit): ".format(END_STRING))
        if len(command) > 0:
            if command == "publish":
                channel = input("enter the channel: ")
                message = input("enter the message: ")
                client.senMsg(channel, message)
                continue
            elif command != END_STRING:
                lastSubscription = command
                print("changing subscription to {0}".format(command))
            else:
                print("exiting now...")
                client.senMsg(lastSubscription, END_STRING)
                break

            msg = client.subscribe(subscription)
