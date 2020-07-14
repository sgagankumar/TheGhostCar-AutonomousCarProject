print("Program Started")

# Import packages
import RPi.GPIO as GPIO
import time
import numpy as np
from keras.models import load_model
import cv2
from firebase import firebase
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

firebase = firebase.FirebaseApplication('https://ghost-car-81f09.firebaseio.com/',None)
print("\n\n\n\n Packages imported")
time.sleep(1)

PAGE="""\
<html>
<head>
<title>Raspberry Pi Camera</title>
</head>
<body>
<center><h1>Car Camera View</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
	def __init__(self):
		self.frame = None
		self.buffer = io.BytesIO()
		self.condition = Condition()
		print("Initialization Done")

	def write(self, buf):
		if buf.startswith(b'\xff\xd8'):
			# New frame, copy the existing buffer's content and notify all
			# clients it's available
			self.buffer.truncate()
			with self.condition:
				self.frame = self.buffer.getvalue()
				self.condition.notify_all()
			self.buffer.seek(0)
		return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
			self.send_response(301)
			self.send_header('Location', '/index.html')
			self.end_headers()
		elif self.path == '/index.html':
			content = PAGE.encode('utf-8')
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.send_header('Content-Length', len(content))
			self.end_headers()
			self.wfile.write(content)
		elif self.path == '/stream.mjpg':
			self.send_response(200)
			self.send_header('Age', 0)
			self.send_header('Cache-Control', 'no-cache, private')
			self.send_header('Pragma', 'no-cache')
			self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
			self.end_headers()
			try:
				while True:
					with output.condition:
						output.condition.wait()
						frame = output.frame
					self.wfile.write(b'--FRAME\r\n')
					self.send_header('Content-Type', 'image/jpeg')
					self.send_header('Content-Length', len(frame))
					self.end_headers()
					self.wfile.write(frame)
					self.wfile.write(b'\r\n')
			except Exception as e:
				logging.warning(
					'Removed streaming client %s: %s',
					self.client_address, str(e))
		else:
			self.send_error(404)
			self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
	allow_reuse_address = True
	daemon_threads = True

# INITIALISATION
# Variables
status = {'Auto_Driving':'InActive', 
			'Steering_Angle':[20,'L'],
			'Traffic_light':True,
			'Obstacle_Ahead':True,
			'Traffic_Sign':'None'}

# Load Nueral Network Model
modelfile = str('model.h5')
print('ML Model Selected : ',modelfile)
model = load_model(modelfile)
time.sleep(1)

# Pin Numbering
en1=32
in1=26
in2=24
in3=22
in4=18
en2=16
ser1=11
ser2=13

# Pins setup
GPIO.setmode(GPIO.BOARD)

# Servo Pins
GPIO.setup(ser1,GPIO.OUT)
GPIO.setup(ser2,GPIO.OUT)
servo1 = GPIO.PWM(ser1,50)
servo2 = GPIO.PWM(ser2,50)

# MotorDriver Pins
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
print("\n\n\n Pin Setup Completed\n")
time.sleep(2)

# Driving Calibration
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p1.ChangeDutyCycle(35)
p2.ChangeDutyCycle(35)
print("Driving System Calibrated\n")
time.sleep(3)

# Steering Caliberation
servo1.start(0)
servo2.start(0)
servo1.ChangeDutyCycle(7)
servo2.ChangeDutyCycle(7)
servo1.ChangeDutyCycle(0)
servo2.ChangeDutyCycle(0)
print("Steering System Calibrated\n\n")
time.sleep(3)


def img_preprocess(img):
	img = img[60:135, :, :]
	img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
	img = cv2.GaussianBlur(img, (3,3), 0)
	img = cv2.resize(img, (200, 66))
	img = img/255
	return img

def steering(frame):
	image = np.asarray(frame)
	image = img_preprocess(image)
	image = np.array([image])
	angle = float(model.predict(image))
	
	avgAngle=0
	if(-12<angle and angle<=12):
		avgAngle=0
	elif(angle>12):
		avgAngle=25
	elif(angle<-12):
		avgAngle=-25
	finalAngle=90+avgAngle
	status['Steering_Angle']=finalAngle

	#Convert predicted angle range to the Servo Angle range
	servo1.ChangeDutyCycle(2+(finalAngle/18))
	servo2.ChangeDutyCycle(2+(finalAngle/18))
	time.sleep(0.5)
	servo1.ChangeDutyCycle(0)
	pass

def obstacle():
	pass

def traffic():
	# Recognise Traffic Light and Traffic Sign
	result = firebase.get('/TRAFFIC_SIGN/','')
	sign = result['Sign']
	status['Traffic_Sign']=sign
	

	pass

def printStatus():
	print(status['Auto_Driving'],status['Steering_Angle'],status['Traffic_light'],status['Obstacle_Ahead'],status['Traffic_Sign'],sep='\t\t')


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
	output = StreamingOutput()
	camera.start_recording(output, format='mjpeg')
	image=np.array((480,640,3),dtype=np.uint8)

	print('Auto_Driving\tSteering_Angle\t\tTraffic_light\tObstacle_Ahead\tTraffic_Sign')
	printStatus()
	time.sleep(3)
	try:
		address = ('', 8000)
		server = StreamingServer(address, StreamingHandler)
		server.serve_forever()

		status['AutoDriving']='Active'
		GPIO.output(in1,GPIO.HIGH)
		GPIO.output(in3,GPIO.HIGH)

		while(cap.isOpened()):
			_, frame = cap.read()
			camera.capture(image,'bgr')
			printStatus()

			# Update Parameters
			steering(image)
			# obstacle()
			# traffic()

finally:

	# Steering Reset
	time.sleep(0.1)
	servo1.ChangeDutyCycle(7)
	servo2.ChangeDutyCycle(7)
	time.sleep(0.2)
	servo1.ChangeDutyCycle(0)
	servo2.ChangeDutyCycle(0)

	time.sleep(0.5)
	servo1.stop()
	servo2.stop()
	p1.stop()
	p2.stop()

	time.sleep(1)
	GPIO.cleanup()
	time.sleep(1)
	camera.stop_recording()
	print('\n\nProgram Ended\n\n')