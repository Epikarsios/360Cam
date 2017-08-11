import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

import time
import atexit

mh = Adafruit_MotorHAT()
shutterPin = 18 # Broadcom pin 18 (P1 pin 12)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(shutterPin, GPIO.OUT) # LED pin set as output

GPIO.output(shutterPin, GPIO.LOW)

def takePic():
	time.sleep(1)
	GPIO.output(shutterPin, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(shutterPin, GPIO.LOW)
	time.sleep(1)
def turnOffMotors():
      mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
      mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
      mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
      mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
      print('Shutting off motors')

atexit.register(turnOffMotors)

CamMotor = mh.getStepper(200, 2)  # 200 steps/rev, motor port #1
CamMotor.setSpeed(10)             # 30 RPM


def ForStep(stepper,numberSteps):
	for i in range (0,numberSteps):
		stepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
	
	turnOffMotors()
def BackStep(stepper,numberSteps):
	
	stepper.step(numberSteps, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
	turnOffMotors()


def rotate360(stepper):
	AmtSteps = input('How many steps between pics?  ')
	totalPics = 1600/(AmtSteps)
	lenMov = (totalPics)/24
	print('This will take %s pics') % totalPics
	print ('Starting in 5 seconds')
	time.sleep(5)
	for i in range (0,totalPics):
		takePic()
		ForStep(CamMotor, AmtSteps)



while True:
	rotate360(CamMotor)
	turnOffMotors()

    
GPIO.cleanup() # cleanup all GPIO
