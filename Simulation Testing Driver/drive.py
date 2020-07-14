from flask import Flask
import socketio
import eventlet
import numpy as np
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2
import sys

modelfile = str(sys.argv[1])
print('Model Selected : ',modelfile)

sio = socketio.Server()

app = Flask(__name__) #'__main__'

def img_preprocess(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3,3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img

speed_limit = 15

# @app.route('/home')
# def greeting():
# 	return 'Welcome!'

@sio.on('telemetry')
def telemetry(sid, data):
	speed = float(data['speed'])
	image = Image.open(BytesIO(base64.b64decode(data['image'])))
	image = np.asarray(image)
	image = img_preprocess(image)
	image = np.array([image])
	steering_angle = float(model.predict(image))
	throttle = 1.0 - speed/speed_limit
	# print('steer:{} throttle:{} speed:{}mph'.format(steering_angle, throttle, speed))
	send_control(steering_angle, throttle)

@sio.on('connect') #other options : message, disconnect
def connect(sid, environ):
	print('\n\n\t\tAutonomous Driving Engaged!\n\n')
	send_control(0,0)

def send_control(steering_angle, throttle):
	sio.emit('steer', data = {
			'steering_angle': steering_angle.__str__(),
			'throttle': throttle.__str__()
		})

if __name__ == '__main__':
	# app.run(port=3000)
	model = load_model(modelfile)
	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('', 4567)), app)