import RPi.GPIO as GPIO
import time
import sys
import os
from subprocess import Popen
os.system('killall omxplayer.bin')
hala = ("/home/pi/Desktop/HALA.mp4")
soaps = ("/home/pi/Desktop/SOAP.mp4")
wash = ("/home/pi/Desktop/WASH.mp4")
blank = ("/home/pi/Desktop/BLANK.mp4")
D1 = 0
D2 = 0
D3 = 0
D4 = 0
presence = 0
soap = 0
water = 0
done = 0
def check():
    global D1
    global D2
    global D3
    global D4
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    # LEFT SENSOR
    TRIG1 = 23
    ECHO1 = 24

    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)

    GPIO.output(TRIG1, False)
    time.sleep(0.1)

    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)
    time.sleep(0.00006)

    while GPIO.input(ECHO1) == 0:
        pulse_start1 = time.time()

    while GPIO.input(ECHO1) == 1:
        pulse_end1 = time.time()

    pulse_duration1 = pulse_end1 - pulse_start1

    distance1 = pulse_duration1 * 17150

    distance1 = round(distance1, 2)

    if distance1 < 100:
        D1 = 1
        print ("D1 close")
    else:
        D1 = 0
    
    print ("D1 scanned")
    time.sleep(0.1)

    GPIO.cleanup()
    
    GPIO.setmode(GPIO.BCM)
    # WATER SENSOR
    TRIG2 = 5
    ECHO2 = 6

    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(ECHO2, GPIO.IN)

    GPIO.output(TRIG2, False)
    time.sleep(0.1)

    GPIO.output(TRIG2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)
    time.sleep(0.00006)

    while GPIO.input(ECHO2) == 0:
        pulse_start2 = time.time()

    while GPIO.input(ECHO2) == 1:
        pulse_end2 = time.time()

    pulse_duration2 = pulse_end2 - pulse_start2

    distance2 = pulse_duration2 * 17150

    distance2 = round(distance2, 2)

    if distance2 < 40:
        D2 = 1
        print ("D2 close")
    else:
        D2 = 0
    
    print ("D2 scanned")

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # SOAP SENSOR
    time.sleep(0.1)

    TRIG3 = 27
    ECHO3 = 22

    GPIO.setup(TRIG3, GPIO.OUT)
    GPIO.setup(ECHO3, GPIO.IN)

    GPIO.output(TRIG3, False)
    time.sleep(0.1)

    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)
    time.sleep(0.00006)

    while GPIO.input(ECHO3) == 0:
        pulse_start3 = time.time()

    while GPIO.input(ECHO3) == 1:
        pulse_end3 = time.time()

    pulse_duration3 = pulse_end3 - pulse_start3

    distance3 = pulse_duration3 * 17150

    distance3 = round(distance3, 2)

    if distance3 < 40:
        D3 = 1
        print ("D3 close")
    else:
        D3 = 0
    
    print ("D3 scanned")

    time.sleep(0.1)
    
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # RIGHT SENSOR
    TRIG4 = 20
    ECHO4 = 21

    GPIO.setup(TRIG4, GPIO.OUT)
    GPIO.setup(ECHO4, GPIO.IN)

    GPIO.output(TRIG4, False)
    time.sleep(0.1)

    GPIO.output(TRIG4, True)
    time.sleep(0.00001)
    GPIO.output(TRIG4, False)
    time.sleep(0.00006)

    pulse_start4 = time.time()

    while GPIO.input(ECHO4) == 0:
        pulse_start4 = time.time()

    while GPIO.input(ECHO4) == 1:
        pulse_end4 = time.time()

    pulse_duration4 = pulse_end4 - pulse_start4

    distance4 = pulse_duration4 * 17150

    distance4 = round(distance4, 2)

    if distance4 < 100:
        D4 = 1
        print ("D4 close")
    else:
        D4 = 0
    
    print ("D4 scanned")

    time.sleep(0.1)

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    print(D1,D2,D3,D4)

x = 1
while True:
    check()
    omxc = Popen(['omxplayer', '-o', 'local', '--loop', blank])
    global WATERPORT
    WATERPORT=16
    if presence==1:
        if done==1:
            presence=0
            soap=0
            while D1==1 and D4==1:
                check()
        else:
            print("HALAAAA")
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', hala])
            time.sleep(8)
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-o', 'local', '--loop', blank])
            presence=0
            
    while D1==1 and D4==1:
        presence=1
        print("Presence",presence)
        check()
        while D3==1:
            soap=1
            check()
        while D2==1:
            #if soap==0:
                #print("SOAP")
                #omxc = Popen(['omxplayer', '-b', soaps])
                #time.sleep(4)
                #os.system('killall omxplayer.bin')
            print("WASH")
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', wash])
            GPIO.setup(WATERPORT,GPIO.OUT)
            GPIO.output(WATERPORT,True)
            time.sleep(27)
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-o', 'local', '--loop', blank])
            presence = 0
            done=1
            check()
        if done==1:
            break
