import numpy as np
import cv2
import os
import sys
import requests
import serial
import time
import math
import detection

def Plotter(txt):
    # Open grbl serial port
    s = serial.Serial(port="COM8", baudrate=115200)
    s.write("\r\n\r\n".encode())
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

    objR = detection.obj_res['predictions'][0]["detection_boxes"]
    objN= detection.obj_res['predictions'][0]["detection_names"]


    def unlock():
        gcode = "$X " + '\n'
        s.write(gcode.encode())
        return "Here is"
    def go():
        gcode = "M3 S255" + '\n'+"G10 P0 L20 X0 Y0 Z0" + '\n'+"G21G91X{}Y-{}F10".format((x1-30)/2.5, (x1-30)/2.5) + '\n' + "G21G91X{}Y{}F10".format(y1/2.5, y1/2.5) + '\n'+"M5" + '\n' +"G21G91X{}Y-{}10".format(wid / 2.5, wid / 2.5) + '\n' + "G21G91X{}Y{}F10".format(hei / 2.5,
                                                                                                 hei / 2.5) + '\n'+ "G21G91X-{}Y{}F10".format(wid/2.5, wid/2.5) + '\n' + "G21G91X-{}Y-{}F10".format(hei/2.5, hei/2.5) + '\n'+"M3 S255" + '\n'
        print(gcode)
        s.write(gcode.encode())
        return(gcode)

    def square():
        gcode = "G21G91X{}Y-{}10".format(wid / 2.5, wid / 2.5) + '\n' + "G21G91X{}Y{}F10".format(hei / 2.5,
                                                                                                 hei / 2.5)
        s.write(gcode.encode())
        time.sleep(10)
        gcode2='\n' + "G21G91X-{}Y{}F10".format(wid / 2.5, wid / 2.5) + '\n' + "G21G91X-{}Y-{}F10".format(hei / 2.5,
                                                                                                     hei / 2.5) + '\n'
        s.write(gcode2.encode())
        return "we draw square"

    def one():
        gcode = "G10 P0 L20 X0 Y0 Z0" + '\n'
        s.write(gcode.encode())
        return "Here is 원점"

    def returnto():
        gcode = "G21G90 G0Z5" + ' \n' + "G90 G0 X0 Y0" + ' \n' + "G90 G0 Z0" + '\n'
        s.write(gcode.encode())
        return "return to 원점"

    def initial():  # 실제 종이랑 플로터 위치 측정 후 시작점 즉 종이 제일 끝 설정하기
        gcode = "G21G91X{}Y-{}F10".format((x1-30)/2.5, (x1-30)/2.5) + '\n' + "G21G91X{}Y{}F10".format(y1/2.5, y1/2.5) + '\n'
        s.write(gcode.encode())
        return "now we have to draw."

    def servo_up():
        gcode = "M3 S255" + '\n'
        s.write(gcode.encode())
        return "펜 들었음~"

    def servo_down():
        gcode = "M5" + '\n'
        s.write(gcode.encode())
        return "펜 내렸음~"
    unlock()
    for i in range(detection.obj_cnt):
        print(objN[i], txt)
        print(txt == objN[i])
        if (txt == objN[i]):
            boxes = objR[i]
            # # location에 크기와 좌표 저장
            # location = []
            x1 = (boxes[0]) * 380.0
            x2 = (boxes[2]) * 297.0
            y1 = (boxes[1]) * 210.0
            y2 = (boxes[3]) * 260.0
            wid = x2 - x1
            hei = y2 - y1
            print(wid,hei)

            servo_up()

            time.sleep(2)

            one()
            time.sleep(2)

            initial()
            time.sleep(2)

            servo_down()
            time.sleep(3)

            square()
            time.sleep(15)

            # squareB()
            # time.sleep(2)


            servo_up()
            time.sleep(2)

            returnto()
            time.sleep(2)


            time.sleep(10)


        else:
            print('no')