#sudo apt-get install python.smbus
#sudo apt-get install i2c-tools
#sudo pip3 install adafruit-circuitpython-servokit

import time
import random
from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

kit = ServoKit(channels=16) #, address=0x40, reference_clock_speed=25000000)

kit.servo[0].angle = 0
kit.servo[1].angle = 0
time.sleep(5)

time.sleep(1)
kit.servo[0].angle = 10
kit.servo[1].angle = 15
time.sleep(1)
kit.servo[0].angle = 20
kit.servo[1].angle = 25
time.sleep(1)
kit.servo[0].angle = 30
kit.servo[1].angle = 45
time.sleep(1)
kit.servo[0].angle = 40
kit.servo[1].angle = 65
time.sleep(1)
kit.servo[0].angle = 50
kit.servo[1].angle = 90
time.sleep(1)
kit.servo[0].angle = 60
kit.servo[1].angle = 110
time.sleep(1)
kit.servo[0].angle = 70
kit.servo[1].angle = 130
time.sleep(1)
kit.servo[0].angle = 80
kit.servo[1].angle = 165

for knee in range(165,45,-4):
    kit.servo[1].angle = knee
    time.sleep(.1)
for knee in range(45,165, 4):
    kit.servo[1].angle = knee
    time.sleep(.1)
for knee in range(165,45,-4):
    kit.servo[1].angle = knee
    time.sleep(.1)

for thigh in range(80,0,-4):
    kit.servo[0].angle = thigh
    time.sleep(.1)
for thigh in range(0,80,4):
    kit.servo[0].angle = thigh
    time.sleep(.1)

for demo in range (1,20):
    kit.servo[0].angle = random.randint(0,80)
    time.sleep(.6)
    kit.servo[1].angle = random.randint(0,165)
    time.sleep(.6)

