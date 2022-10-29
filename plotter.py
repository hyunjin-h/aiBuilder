import numpy as np
import cv2
import os
import sys
import requests
import serial
import time
import math
import detection




def Plotter(od_num):
    # 사진을 object detection
    boxes=detection.obj_res['predictions'][0]["detection_boxes"][od_num]
    print(boxes)
    # location에 크기와 좌표 저장
    location = []
    x1 = (boxes[0]) * 380
    x2 = (boxes[2]) * 297
    y1 = (boxes[1]) * 210
    y2 = (boxes[3]) * 260
    wid = x2 - x1
    hei = y2 - y1
    coord = [x1, x2, y1, y2, wid, hei]
    location.append(coord)

    # Open grbl serial port
    s = serial.Serial(port="COM7", baudrate=115200)

    # Wake up grbl
    s.write("\r\n\r\n".encode())
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input


    def square():
        gcode = "G21G91G1X{}Y-{}F2000".format(wid, wid) + '\n' + "G21G91G1X{}Y{}F2000".format(hei,
                                                                                              hei) + '\n' + "G21G91G1X-{}Y{}F2000".format(
            wid, wid) + '\n' + "G21G91G1X-{}Y-{}F1000".format(hei, hei) + '\n'
        s.write(gcode.encode())
        return "we draw square"

    def one():
        gcode = "G10 P0 L20 X0 Y0 Z0" + '\n'
        s.write(gcode.encode())
        return "Here is 원점"

    def returnto():
        gcode = "G21G90G0Z5" + ' \n' + "G90G0X0Y0" + ' \n' + "G90G0Z0 " + '\n'
        s.write(gcode.encode())
        return "return to 원점"

    def initial():  # 실제 종이랑 플로터 위치 측정 후 시작점 즉 종이 제일 끝 설정하기
        gcode = "G21G91G1X{}Y-{}F3000".format(x1 - 30, x1 - 30) + '\n' + "G21G91G1X{}Y{}F3000".format(y1, y1) + '\n'
        s.write(gcode.encode())
        return "now we have to draw."

    one()
    initial()
    square()
    returnto()