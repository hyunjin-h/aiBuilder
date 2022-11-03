import numpy as np
import cv2
import os
import sys
import requests
import serial
import time
import math
import detection

s = serial.Serial(port="COM8", baudrate=115200)
s.write("\r\n\r\n".encode())
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
def unlock():
    gcode = "$X " + '\n'
    s.write(gcode.encode())
    return "Here is"
def one():
    gcode = "G10 P0 L20 X0 Y0 Z0" + '\n'
    print(gcode)
    time.sleep(3)
    s.write(gcode.encode())
    print(gcode.encode())
    return "Here is"


def returnto():
    gcode = "G21G91X10Y-10F20 "+ '\n'
    print(gcode)
    s.write(gcode.encode())
    print(gcode.encode())
    return "return to"

#
# def initial():  # 실제 종이랑 플로터 위치 측정 후 시작점 즉 종이 제일 끝 설정하기
#     gcode = "G21G91G1X{}Y-{}F3000".format(x1 - 30, x1 - 30) + '\n' + "G21G91G1X{}Y{}F3000".format(y1, y1) + '\n'
#     s.write(gcode.encode())
#     return "now we have to draw."


# def servo_up():
#     gcode="M3 S255"+'\n'
#     s.write(gcode.encode())
#     return "펜 들었음~"
#
# def servo_down():
#     gcode="M5"+'\n'
#     s.write(gcode.encode())
#     return "펜 내렸음~"
unlock()
returnto()





