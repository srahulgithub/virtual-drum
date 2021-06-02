#importing important libraries
import numpy as np
import time
import cv2
from pygame import mixer

# This function plays the corresponding drum beat if a black color object is detected in the region
def play_beat(detected,sound):

	# Checks if the detected black color is greater that a preset value 	
	play = (detected) > hat_thickness[0]*hat_thickness[1]*0.8

	# If it is detected play the corresponding drum beat
	if play and sound==1:
		drum_snare.play()
		
	elif play and sound==2:
		drum_hat.play()
		time.sleep(0.001)

	elif play and sound==3:
		drum_stick.play() 

	elif play and sound==4:
		drum_bass.play() 	

	elif play and sound==5:
		drum_tom.play() 		


# This function is used to check if black color is present in the small region
def detect_in_region(frame,sound):
	
	# Converting to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Creating mask
	mask = cv2.inRange(hsv, blackLower, blackUpper)
	
	# Calculating the number of black pixels
	detected = np.sum(mask)
	
	# Call the function to play the drum beat
	play_beat(detected,sound)

	return mask

# A flag variable to choose whether to show the region that is being detected
blank = False

# Importing drum beats
mixer.init()
drum_hat = mixer.Sound('./sounds/Hi-Hat.mp3')
drum_snare = mixer.Sound('./sounds/Snare-Drum.mp3')
drum_stick = mixer.Sound('./sounds/Drum_stick.mp3')
drum_bass = mixer.Sound('./sounds/Bass-Drum.mp3')
drum_tom = mixer.Sound('./sounds/Floor-Tom-Drum.mp3')

# Set HSV range for detecting black color 
blackLower = (0,0,0)
blackUpper = (180,255,0)

# Obtain input from the webcam 
camera = cv2.VideoCapture(0)
ret,frame = camera.read()
H,W = frame.shape[:2]

kernel = np.ones((7,7),np.uint8)

# Read the image of High Hat,Snare drum,tom-tom,bass drum and stick.
hat = cv2.resize(cv2.imread('./images/high_hat.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)
snare = cv2.resize(cv2.imread('./images/snare_drum.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)
stick = cv2.resize(cv2.imread('./images/stick.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)
bass = cv2.resize(cv2.imread('./images/bass_drum.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)
tom = cv2.resize(cv2.imread('./images/tom_tom.jpg'),(200,100),interpolation=cv2.INTER_CUBIC)

# Set the region area for detecting black color 
hat_center = [np.shape(frame)[1]*4//8,np.shape(frame)[0]*4//8]
snare_center = [np.shape(frame)[1]*6//8,np.shape(frame)[0]*6//8]
stick_center = [np.shape(frame)[1]*2//8,np.shape(frame)[0]*2//8]
bass_center = [np.shape(frame)[1]*6//8,np.shape(frame)[0]*2//8]
tom_center = [np.shape(frame)[1]*2//8,np.shape(frame)[0]*6//8]

hat_thickness = [200,100]
hat_top = [hat_center[0]-hat_thickness[0]//2,hat_center[1]-hat_thickness[1]//2]
hat_btm = [hat_center[0]+hat_thickness[0]//2,hat_center[1]+hat_thickness[1]//2]

snare_thickness = [200,100]
snare_top = [snare_center[0]-snare_thickness[0]//2,snare_center[1]-snare_thickness[1]//2]
snare_btm = [snare_center[0]+snare_thickness[0]//2,snare_center[1]+snare_thickness[1]//2]

stick_thickness = [200,100]
stick_top = [stick_center[0]-stick_thickness[0]//2,stick_center[1]-stick_thickness[1]//2]
stick_btm = [stick_center[0]+stick_thickness[0]//2,stick_center[1]+stick_thickness[1]//2]

bass_thickness = [200,100]
bass_top = [bass_center[0]-bass_thickness[0]//2,bass_center[1]-bass_thickness[1]//2]
bass_btm = [bass_center[0]+bass_thickness[0]//2,bass_center[1]+bass_thickness[1]//2]

tom_thickness = [200,100]
tom_top = [tom_center[0]-tom_thickness[0]//2,tom_center[1]-tom_thickness[1]//2]
tom_btm = [tom_center[0]+tom_thickness[0]//2,tom_center[1]+tom_thickness[1]//2]

time.sleep(1)

while True:
	
	# Select the current frame
	ret, frame = camera.read()
	frame = cv2.flip(frame,1)

	if not(ret):
	    break
    
	# Select region corresponding to the Snare drum
	snare_region = np.copy(frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]])
	mask = detect_in_region(snare_region,1)

	# Select region corresponding to the High Hat
	hat_region = np.copy(frame[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]])
	mask = detect_in_region(hat_region,2)

	# Select region corresponding to the stick
	stick_region = np.copy(frame[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]])
	mask = detect_in_region(stick_region,3)

    # Select region corresponding to the bass drum
	bass_region = np.copy(frame[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]])
	mask = detect_in_region(bass_region,4)

    # Select region corresponding to the tom-tom drum
	tom_region = np.copy(frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]])
	mask = detect_in_region(tom_region,5)

	# Output project title
	cv2.putText(frame,'VIRTUAL DRUMS',(10,30),2,1,(20,20,20),3)
    
	# If flag is selected, display the region under detection
	if blank:
		frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]] = cv2.bitwise_and(frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]],frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]], mask=mask[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]])
		frame[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]] = cv2.bitwise_and(frame[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]],frame[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]],mask=mask[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]])
		frame[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]] = cv2.bitwise_and(frame[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]],frame[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]],mask=mask[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]])
		frame[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]] = cv2.bitwise_and(frame[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]],frame[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]],mask=mask[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]])
		frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]] = cv2.bitwise_and(frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]],frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]],mask=mask[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]])

	# If flag is not selected, display the drums
	else:
		frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]] = cv2.addWeighted(snare, 1, frame[snare_top[1]:snare_btm[1],snare_top[0]:snare_btm[0]], 1, 0)
		frame[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]] = cv2.addWeighted(hat, 1, frame[hat_top[1]:hat_btm[1],hat_top[0]:hat_btm[0]], 1, 0)
		frame[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]] = cv2.addWeighted(stick, 1, frame[stick_top[1]:stick_btm[1],stick_top[0]:stick_btm[0]], 1, 0)
		frame[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]] = cv2.addWeighted(bass, 1, frame[bass_top[1]:bass_btm[1],bass_top[0]:bass_btm[0]], 1, 0)
		frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]] = cv2.addWeighted(tom, 1, frame[tom_top[1]:tom_btm[1],tom_top[0]:tom_btm[0]], 1, 0)
    
	cv2.imshow('Output',frame)
	key = cv2.waitKey(1) & 0xFF
	# 'Q' to exit
	if key == ord("q"):
		break
 
# Clean up the open windows
camera.release()
cv2.destroyAllWindows()