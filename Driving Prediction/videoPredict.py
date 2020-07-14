import cv2
from keras.models import load_model
import time
import numpy as np

def img_preprocess(img):
	# cv2.imshow('process',img)
	img = img[80:159, :, :]
	img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
	img = cv2.GaussianBlur(img, (3,3), 0)
	img = cv2.resize(img, (200, 66))
	# cv2.imshow('postprocess',img)
	img = img/255
	return img

def main():
	modelfile = str('model.h5')
	print('ML Model Selected : ',modelfile)
	model = load_model(modelfile)
	time.sleep(1)

	vidcap = cv2.VideoCapture('http://192.168.43.222:8000/stream.mjpg') #'http://192.168.43.222:8000/stream.mjpg'


	while True:
		_,frame = vidcap.read()
		cv2.imshow('Result', frame)
		frame = cv2.resize(frame, (320, 160))
		image = np.asarray(frame)
		image = img_preprocess(image)
		image = np.array([image])
		angle = float(model.predict(image))
		avgAngle=0
		time.sleep(0.1)
		if(-15<angle and angle<=15):
			avgAngle=0
		elif(angle>15):
			avgAngle=25
		elif(angle<-15):
			avgAngle=-25
		print('Angle: ',angle,'\tAvg. Angle: ', avgAngle,'...',end='\r')
		# avgAngle=input("enter:")
		file1=open('angle.txt','w')
		file1.write(str(avgAngle))

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	file1.close()
	vidcap.release()
	cv2.destroyAllWindows()

main()