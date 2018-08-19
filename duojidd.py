#!/usr/bin/env python3
# -*- coding:utf-8 -*
import serial

def __exchange(a):
    n = round((1500 + (a / 180) * 2000) % 256)  # 计算16进制数低八位
    m = int((1500 + (a / 180) * 2000) / 256)  # 计算16进制高八位
    #k = round((1500 + (b / 180) * 2000) % 256)  # 计算16进制数低八位
    #j = int((1500 + (b / 180) * 2000) / 256)  # 计算16进制高八位
    return (n,m)

def duojidd(alpha1, alpha2):
    n, m = __exchange(alpha1)
    k, j = __exchange(alpha2)
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
    ser.close()
    ser.open()
    """
    指令名 CMD_ SERVO_MOVE 指令值 3 数据长度 Length：  
    说明：控制任意个舵机的转动，数据长度 Length =控制舵机的个数×3+5  
    参数 1：要控制舵机的个数 
    参数 2：时间低八位 
    参数 3：时间高八位  
    参数 4：舵机 ID 号 
    参数 5：角度位置低八位 
    参数 6：角度位置高八位 
    参数......：格式与参数 4,5,6 相同，控制不同 ID 的角度位置。 
    """
    cmd = [0x55, 0x55, 0x0B, 0x03, 0x02, 0xe8, 0x03, 0x03, n, m, 0x06, k, j]
    print(alpha1, ":", (1500 + (alpha1 / 180) * 2000), alpha2, ":", (1500 + (alpha2 / 180) * 2000), cmd)
    ser.write(cmd)
    try:
       for i in range(1, 5):
             response = ser.read()
             print(response)
             #sleep(1)
    except KeyboardInterrupt:
         ser.close()


#duojidd(30, 20)

import sys
if len(sys.argv)>2:
   duojidd(int(sys.argv[1]), int(sys.argv[2]) )