import serial
import time



def servo(in_data):
    s = serial.Serial(port="COM9", baudrate=115200)

    print(s.name)
    # Wake up grbl
    """s.write("\r\n\r\n".encode())
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input"""
    pos = 20
    if serial.available():
        if (in_data == '1'):
            pos += 80
            if (pos == 180):
                pos = 20
        else:
            pos = 20
        s.write(pos.encode())


servo(1)
