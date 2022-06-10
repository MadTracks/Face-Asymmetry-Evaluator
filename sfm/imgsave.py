import cv2
import keyboard
from time import sleep
import os


	
	

vid = cv2.VideoCapture(0)
imgct=0
cwd = os.getcwd()
os.chdir('./images')

while(True):
      
    ret, frame = vid.read()
    if keyboard.is_pressed('q'):
        print("Checking")
        cv2.imwrite(str(imgct)+".jpg",frame)
        imgct+=1
        sleep(0.5)
    elif keyboard.is_pressed('esc'):
        break
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
  
# After the loop release the cap object
vid.release()
os.chdir(cwd)
# Destroy all the windows
cv2.destroyAllWindows()
