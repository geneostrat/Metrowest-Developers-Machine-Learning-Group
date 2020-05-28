# Servo Control
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
pwmThigh = GPIO.PWM(15, 50)
pwmThigh.stop()
pwmThigh.start(2)

#pwmKnee = GPIO.PWM(3, 50)
#pwmKnee.stop()
#pwmKnee.start(.1)
#sleep(1)
#pwmKnee.stop()
#GPIO.output(3, False)
#GPIO.cleanup()

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(5, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(5, False)
    pwm.ChangeDutyCycle(0)