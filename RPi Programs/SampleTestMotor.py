print('Program Started')
import RPi.GPIO as GPIO
import time

print('GPIO Ready')
in1=22
in2=24
in3=26
in4=32
en1=16
en2=18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
p1=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)
p1.start(en1)
p2.start(en2)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
time.sleep(10)
try:
        print('Motor Runnning')
        while True:
                p1.ChangeDutyCycle(35)
                p2.ChangeDutyCycle(35)

                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                time.sleep(10)
finally:
        p1.stop()
        p2.stop()
        GPIO.cleanup()
        print('Program Ended')
