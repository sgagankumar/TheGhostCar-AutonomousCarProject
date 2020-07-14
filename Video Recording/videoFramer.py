import cv2

f=open('driving_log.csv', 'w')
vidcap = cv2.VideoCapture('output.avi')
count=0
while True:
	_,frame = vidcap.read()
	cv2.imshow('Result', frame)
	count+=1
	cv2.imwrite('IMG/file'+str(count)+'.jpg',frame)
	line='IMG/file'+str(count)+'.jpg,0\n'
	f.write(line)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

vidcap.release()
cv2.destroyAllWindows()
f.close()