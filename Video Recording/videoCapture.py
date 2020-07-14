import cv2
from datetime import datetime 

vidcap = cv2.VideoCapture('http://192.168.1.2:8000/stream.mjpg') #Replace with the stream URL
fps = vidcap.get(cv2.CAP_PROP_FPS)
width = vidcap.get(3)
height = vidcap.get(4)

# Define the codec and create VideoWriter object
outputFileName = 'output_'+str(datetime.now().time())+'.avi'
outputFileName = outputFileName.replace(':','_')
outputFileName = outputFileName.replace('.','_',1)
print('OUTPUT FILE:',outputFileName)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#Replace width, height with desired recording clarity
out = cv2.VideoWriter(outputFileName,fourcc, fps , (width,height))

while (vidcap.isOpened()):
	success,frame = vidcap.read()
	cv2.imshow('Result', image)
	#Write to video
	out.write(image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

vidcap.release()
cv2.destroyAllWindows()