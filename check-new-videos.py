### main_program_v3.py -- 12-02-2020 -- Andrew R Gross

### Libraries
import pygame
import time
import cv2
import RPi.GPIO as GPIO
import glob
#import numpy as np
#from ffpyplayer.player import MediaPlayer
#import vlc
import io,sys,os,subprocess
global process

### Declare variables and assets
## Images
searching = pygame.image.load('/home/pi/Rocket-dashboard/Images/searching-for-transmission.png')
play_latest = pygame.image.load('/home/pi/Rocket-dashboard/Images/new-message.png')
proceed = pygame.image.load('/home/pi/Rocket-dashboard/Images/continue.png')

"""
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
"""

def get_video_duration(path):
        vidcapture = cv2.VideoCapture(path)
        fps = vidcapture.get(cv2.CAP_PROP_FPS)
        totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT);
        durationInSeconds = float(totalNoFrames) / float(fps)
        return(durationInSeconds)

## Videos
full_video_list = glob.glob('/home/pi/Rocket-dashboard/Videos/*')
full_video_list.sort(key=os.path.getmtime, reverse = True)
video_list = full_video_list[0:4]
print(video_list)

#color_list = ((255,0,255), (255,0,127), (255,0,0), (255,127,0))
### Add a system for sorting just the most recent for videos

## Pins
button1 = 2
button2 = 3

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(button1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN, pull_up_down=GPIO.PUD_UP)

screenstate = 0


print('Setup complete. Running test')

### Main Program Body
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.blit(searching, (0,0))

font = pygame.font.SysFont(None, 50)

screen.blit(play_latest, (0,0))
new_video = (1,2)

if len(new_video) >0:
	text1 = font.render('NEW TRANSMISSION RECEIVED', True, (255,102,178))
	screen.blit(text1, (50, 30))
	pygame.display.update()
	#time.sleep(0.5)
while True:
	#text1 = font.render('Play latest message or skip', True, (152,255,54))
	#screen.blit(text1, (50, 260))
	#pygame.display.update()
	if GPIO.input(button1) == False:	# Play message
		print('Initializing delayed start')

		pygame.quit()
		print('Playing '+video_list[0])
		durationInSeconds = get_video_duration(video_list[0])
		print(str(durationInSeconds) + ' seconds')
		print('Begining delayed startup')
		subprocess.Popen(['/home/pi/Rocket-dashboard/start-main-program.sh', str(round(durationInSeconds)+1)])
		print('Delayed startup running. Playing video and then exiting')
		subprocess.Popen(['vlc',video_list[0],'--play-and-exit'])
		print('Ending current program!')
		pygame.quit()
		quit()

		#subprocess.Popen(['/home/pi/Rocket-dashboard/start-main-program.sh', duration])
		print('Beginning video')
		#subprocess.Popen
		print('Quiting')
		break

	if GPIO.input(button2) == False: 	# If button 2 is pressed, skip
	#	print('Initializing start without delay')
		subprocess.Popen(['/home/pi/Rocket-dashboard/start-main-program.sh', '0'])
		#
		break

print('Exiting startup sequence')
pygame.quit()
quit()

"""

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
                        elif screenstate == 3:		# If on the radio select screen, play selected video
                                #chirp.play()
                                pygame.quit()
                                #video_file = video_list[0]
#                                PlayVideo(video_file)
                                print('Playing '+video_file)
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
except:
        GPIO.cleanup()
        print('exception called?')
        raise
#        quit()
"""
