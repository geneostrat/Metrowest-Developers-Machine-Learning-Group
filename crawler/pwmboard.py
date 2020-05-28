import os
import time
import wiringpi # sudo pip3 wiringpi2

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(15,2)
wiringpi.pwmSetMode(0)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(500)
wiringpi.pwmWrite(15,0)
