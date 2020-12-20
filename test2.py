### main_program_v3.py -- 12-02-2020 -- Andrew R Gross

### Libraries
import pygame
import time
import cv2
import RPi.GPIO as GPIO
import glob
import numpy as np
from ffpyplayer.player import MediaPlayer
import vlc
import subprocess

#from os import listdir
#from os.path import isfile, join

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill((255, 255, 255))
# Draw a solid blue circle in the center
pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
### Declare variables and assets
## Images
menucontrol = pygame.image.load('/home/pi/Rocket-dashboard/Images/menu-control.png')
menuradio = pygame.image.load('/home/pi/Rocket-dashboard/Images/menu-radio.png')
win_space = pygame.image.load('/home/pi/Rocket-dashboard/Images/win-deepspace.png')
win_mars = pygame.image.load('/home/pi/Rocket-dashboard/Images/win-mars.png')
win_orbit = pygame.image.load('/home/pi/Rocket-dashboard/Images/win-orbit.png')
win_vents = pygame.image.load('/home/pi/Rocket-dashboard/Images/win-vents.png')
win_hole = pygame.image.load('/home/pi/Rocket-dashboard/Images/win-observatory.png')
## Sounds
beep1 = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/beep1.wav')
beep2 = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/beep2.wav')
bip = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/bip.wav')
biz = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/biz.wav')
bloop = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/bloop.wav')
blorp = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/blorp.wav')
boop = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/boop.wav')
buzz = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/buzz.wav')
chirp = pygame.mixer.Sound('/home/pi/Rocket-dashboard/Sounds/chirp.wav')
## Videos
full_video_list = glob.glob('/home/pi/Rocket-dashboard/Videos/*')
video_list = full_video_list[0:4]

color_list = ((255,0,255), (255,0,127), (255,0,0), (255,127,0))
### Add a system for sorting just the most recent for videos

## Pins
button1 = 2
button2 = 3
button3 = 25
#button4
switch1 = 4
switch2 = 17
switch3 = 27
switch4 = 22
## LEDs
led1 = 9
led2 = 1
led3 = 1
led4 = 1

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(button1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(button3,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(button4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch3,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(led1,GPIO.OUT)

screenstate = 0

switch1state = True
switch2state = True
switch3state = True
switch4state = True
light1color = (230,240,230)
light2color = (230,230,240)
light3color = (240,230,230)
switch4color = (130, 130, 130)
rollingvalue = 20
modifier = 1

window_list = (win_orbit, win_mars, win_space, win_hole, win_vents)
current_window = 1
# 
#ffpyplayer for playing audio

def PlayVideo(video_path):
	cap = cv2.VideoCapture(video_path)
	if (cap.isOpened()==False):
		print('Error opening video file')
	while(cap.isOpened()):
		### capture frame-by-frame
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow('Frame', frame)
			if GPIO.input(button1) == False:
				break
		else:
			break
	cap.release()
	cv2.destroyAllWindows()
	print('video complete')

"""
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    while True:
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break
        cv2.namedWindow("Video")
        cv2.moveWindow("Video", 0, 0)
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()
"""
#PlayVideo(video_path)

print('Setup complete. Running test')

screen.blit(menucontrol, (0,0))
pygame.display.update()
try:
        while True:
#               time.sleep(0.1)
                ### Button1: Select
                if GPIO.input(button1) == False:
                        beep1.play()
                        print('b1 pressed')
                        if GPIO.input(button2) == False:
                                print('button1-2 pressed')
                                pygame.quit()
                                quit()
                        elif screenstate == 0:	# If on the control-menu screen:
                                print('ss = 0')
				### Draw dashboard
                                screen.fill((255,255,250))
                                pygame.draw.circle(screen, (230,255,230), (130,370), 50)
                                pygame.draw.circle(screen, (  0,  0,  0), (130,370), 51, 15) # Ring
                                pygame.draw.circle(screen, (255,230,210), (370,370), 50)
                                pygame.draw.circle(screen, (  0,  0,  0), (370,370), 51, 15)
                                pygame.draw.circle(screen, (255,230,210), (610,370), 50)
                                pygame.draw.circle(screen, (  0,  0,  0), (610,370), 51, 15)
                                pygame.draw.rect(screen, (100,100,100), (50,300,640,150), 26)
                                screen.blit(win_orbit,(30,7))
                                screenstate = 2
                              #  pygame.display.update()
                                time.sleep(0.6)
                        elif screenstate == 1:	# If on the radio menu screen:

                                screen.fill((10,10,10))
                                font = pygame.font.SysFont(None, 66)
                                font2 = pygame.font.SysFont(None, 50)
                                text1 = font.render(video_list[0].split('/')[-1], True, color_list[0])
                                text2 = font2.render(video_list[1].split('/')[-1], True, color_list[1])
                                text3 = font2.render(video_list[2].split('/')[-1], True, color_list[2])
                                text4 = font2.render(video_list[3].split('/')[-1], True, color_list[3])
                                screen.blit(text1, (30, 50))
                                screen.blit(text2, (60, 160))
                                screen.blit(text3, (60, 260))
                                screen.blit(text4, (60, 360))
                                pygame.draw.rect(screen, (230,230,200), (10,10,640,130), 9)

                                screenstate = 3
  #                              pygame.display.update()
                        elif screenstate == 2:
                                screen.blit(menucontrol, (0,0))
                                screenstate = 0
                        elif screenstate == 3:		# If on the radio select screen, play selected video
                              #  chirp.play()
                                pygame.quit()
                                video_file = video_list[0]
#                                PlayVideo(video_file)
                                print('Playing '+video_file)
                                subprocess.call(['vlc',video_file,'--play-and-exit'])
#                                PlayVideo(video_list[0])
                               # media_player = vlc.MediaPlayer() 
                                #media_player = vlc.MediaPlayer() 
                         #       vid = vlc.Media(video_file)
                          #      media_player.set_media(vid)
                           #     media_player.play()

                                pygame.init()
                                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                screen.blit(menucontrol, (0,0))
                                screenstate = 0
  #                              pygame.display.update()
                        pygame.display.update()
                        time.sleep(0.5)
                ### Button2: Cycle
                if GPIO.input(button2) == False:
                        bloop.play()
                        print('b2 pressed')
                        if GPIO.input(button1) == False:
                                print('b2-1 pressed')
                                pygame.quit()
                                quit()
                        elif screenstate == 0:	# If on control menu screen, switch to radio menu
                                screen.blit(menuradio, (0,0))
                                screenstate = 1
                        elif screenstate == 1:	# If on radio menu scree, switch to control menu
                                screen.blit(menucontrol, (0,0))
                                screenstate = 0
                        elif screenstate == 2:	# If on dashboard, cycle windows
                                current_window = current_window+1
                                if current_window == len(window_list):
                                        current_window = 0
                                screen.blit(window_list[current_window], (30,7))
                                print(window_list[current_window])
                        elif screenstate == 3: # If on video select screen
                                ### Rotate video order and color
                                video_list = (video_list[1], video_list[2], video_list[3], video_list[0])
                                color_list = (color_list[1], color_list[2], color_list[3], color_list[0])

                                screen.fill((10,10,10))
                                font = pygame.font.SysFont(None, 66)
                                font2 = pygame.font.SysFont(None, 50)
                                text1 = font.render(video_list[0].split('/')[-1], True, color_list[0])
                                text2 = font2.render(video_list[1].split('/')[-1], True, color_list[1])
                                text3 = font2.render(video_list[2].split('/')[-1], True, color_list[2])
                                text4 = font2.render(video_list[3].split('/')[-1], True, color_list[3])
                                screen.blit(text1, (30, 50))
                                screen.blit(text2, (60, 160))
                                screen.blit(text3, (60, 260))
                                screen.blit(text4, (60, 360))
                                pygame.draw.rect(screen, (230,230,200), (10,10,640,130), 9)

                        else:
                                pass
                        pygame.display.update()
                        time.sleep(0.5)
                ### Switch1: Light 1
                if switch1state != GPIO.input(switch1):
                         beep2.play()
                         print('switch1 thrown')
#                         GPIO.output(led1, switch1state)
                         if switch1state == True:
                                 light1color = (255,94,0)  # Safety Orange
                         else:
                                 light1color = (255,231,184) # Peach
                         if screenstate == 2:
                                 pygame.draw.circle(screen, (light1color), (130,370), 40)
                                 pygame.draw.circle(screen, (150,150,150), (130,370), 42, 6)

                                 print("Updating because we're on screenstate2")
                                 pygame.display.update()
                         switch1state = GPIO.input(switch1)
                ### Switch2: Light 2
                if GPIO.input(switch2) != switch2state:
                         biz.play()
                         print('Switch2 thrown')
#                         GPIO.output(led1, switch1state)
                         if switch2state == True:
                                 light2color = (68,0,255)
#                                 pygame.draw.circle(screen, (208,255,230), (370,370), 40)
                         else:
                                 light2color = (201,212,255)
#                                 pygame.draw.circle(screen, (10, 255, 15), (370,370), 40)
#                         pygame.draw.circle(screen, (0, 255, 10), (370,370), 41, 6)
                         if screenstate == 2:
                                 pygame.draw.circle(screen, light2color, (370,370), 40)
                                 pygame.draw.circle(screen, (100,100,100), (370,370), 42, 6)
                                 pygame.display.update()
                         switch2state = GPIO.input(switch2)

                ### Switch3
                if GPIO.input(switch3) != switch3state:
                         boop.play()
                         print('Switch3 thrown')
                         if switch3state == True:
                                 switch3color = (10,255,15)
#                                 pygame.draw.circle(screen, (208,255,230), (610,370), 40)
                         else:
 #                                pygame.draw.circle(screen, (10, 255, 15), (610,370), 40)
                                  switch3color = (208, 255, 230)
                         pygame.draw.circle(screen, (switch3color), (610,370), 40)
                         pygame.draw.circle(screen, (0, 255, 10), (610,370), 41, 6)
                         if screenstate == 2:
                                 pygame.display.update()
                         switch3state = GPIO.input(switch3)
                ### Switch4
                if GPIO.input(switch4) != switch4state:
                         bip.play()
                         print('Switch4 thrown!')
                         if switch4state == True:
                                 switch4color = (230,  0,  0)
#                                 pygame.draw.rect(screen, (20,20,255), (50,300,650,150), 16)
                         else:
                                 switch4color = (255,150,130)
 #                                pygame.draw.rect(screen, (200,200,255), (50,300,650,150), 16)
                         if screenstate == 2:
                                 print('Updating to new color')
                                 pygame.draw.rect(screen, (switch4color), (50,300,640,150), 16)
                                 pygame.display.update()
                         time.sleep(0.5)
                         switch4state = GPIO.input(switch4)
                ### Button3
#                if GPIO.input(button3) == False:
 #                        if rollingvalue == 254:
  #                               modifier = -1
   #                      if rollingvalue == 5:
    #                             modifier = 1
     #                    rollingvalue = rollingvalue + modifier
      #                   button3color = (10,rollingvalue,0)
       #                  pygame.draw.polygon(screen, button3color, [(600,150),(680,200),(680,100)])
        #                 pygame.display.update()

#                         pygame.draw.rect(screen, (200,200,255), (100,300,600,150), 6)

  #              else:
 #                       pass
#        pass
# Import and initialize the pygame library
# Set up the drawing window
#pygame.quit()
except:
        GPIO.cleanup()
        print('exception called?')
        raise
#        quit()
