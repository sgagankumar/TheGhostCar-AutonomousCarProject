import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PMV(11,50)

servo1.start(0)			# pulse off

try:
	while True:
		angle = float(input('Enter angle:'))
		servo1.ChangeDutyCycle(2+(angle/18))
		time.sleep(0.5)
		servo1.ChangeDutyCycle(0)	# to halt
finally:
	servo1.stop()
	GPIO.cleanup()
	print('Program Ended')