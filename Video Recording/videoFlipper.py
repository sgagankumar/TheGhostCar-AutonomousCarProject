import cv2
from datetime import datetime 

vidcap = cv2.VideoCapture('output.avi')
fps = vidcap.get(cv2.CAP_PROP_FPS)
width = vidcap.get(3)  # float
height = vidcap.get(4) # float

outputFileName = 'output_'+str(datetime.now().time())+'_flip.avi'
outputFileName = outputFileName.replace(':','_')
outputFileName = outputFileName.replace('.','_',1)
print('OUTPUT FILE:',outputFileName)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(outputFileName,fourcc, fps , (320,160))

while True:
	_,frame = vidcap.read()
	frame=cv2.flip(frame,1)
	cv2.imshow('Result', frame)
	out.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

vidcap.release()
cv2.destroyAllWindows()
f.close()