
import json
def buildMsg(imageInfo):
    msgDict = {}


    msgDict["from"] = "VIDEO"
    msgDict["type"] = "VIDEOINFO"
    msgDict["data"] = imageInfo
    return json.dumps(msgDict)



def buildMotorMsg(motorAngle):
    motorMsg = {}
    motorMsg["from"] = "AngleCaculator"
    motorMsg["type"] = "SETANGLE"
    motorMsg["data"] = motorAngle

    return json.dumps(motorMsg)