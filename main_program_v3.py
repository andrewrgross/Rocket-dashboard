### main_program_v3.py -- 12-02-2020 -- Andrew R Gross

### Libraries
import pygame
import time
import cv2
import RPi.GPIO as GPIO
import glob
import numpy as np
from ffpyplayer.player import MediaPlayer

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
video_list = full_video_list[0:3]

## Pins
button1 = 2
button2 = 3
button3 = 10
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
GPIO.setup(switch1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(button4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led1,GPIO.OUT)

screenstate = 0

switch1state = True
switch2state = True
light1color = (230,240,230)
light2color = (230,230,240)
light3color = (240,230,230)
switch1_color = (235,182,219)

window_list = (win_orbit, win_mars, win_space, win_hole, win_vents)
current_window = 1
# 
#ffpyplayer for playing audio

def PlayVideo(video_path):
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
            #audio
            img, t = audio_frame
    video.release()
    cv2.destroyAllWindows()

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
                                pygame.draw.circle(screen, (208,255,230), (370,150), 17)
                                pygame.draw.circle(screen, (0, 255, 10), (370,150), 18, 6)
                                pygame.draw.rect(screen, (200,200,255), (300,100,100,600), 6)
                                screen.blit(win_orbit,(30,7))
                                screenstate = 2
                              #  pygame.display.update()
                                time.sleep(0.6)
                        elif screenstate == 1:	# If on the radio menu screen:
                                pygame.quit()
                                video_file = video_list[0]
                                PlayVideo(video_file)
                                pygame.init()
                                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                screen.blit(menu-control, (0,0))
  #                              pygame.display.update()
                        elif screenstate == 2:
                                screen.blit(menucontrol, (0,0))
                                screenstate = 0
                        pygame.display.update()
                        time.sleep(0.5)
                ### Button2: Cycle
                if GPIO.input(button2) == False:
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
                        else:
                                pass
                        pygame.display.update()
                        time.sleep(0.5)
                ### Switch1: Light 1
                if switch1state != GPIO.input(switch1):
                         print('switch1 thrown')
                         GPIO.output(led1, switch1state)
                ### Switch2: Light 2
                ###
  #              else:
 #                       pass
#        pass
# Import and initialize the pygame library
# Set up the drawing window
#pygame.quit()
except:
        print('exception called?')
        raise
#        quit()
