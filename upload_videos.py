### upload_videos.py -- Andrew R Gross -- 2020-12-19

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

## Pins
button1 = 2
button2 = 3

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(button1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN, pull_up_down=GPIO.PUD_UP)

screenstate = 0


print('Setup complete. Running test')



### Main program



print('Checking for new videos')

### List local videos
vid_local = os.listdir('/home/pi/Rocket-dashboard/Videos/')

### Create list of remote videos
os.system('rclone lsf test5:/mobile_one/>/home/pi/Rocket-dashboard/new_videos')
new_videos = open('/home/pi/Rocket-dashboard/new_videos','r')
vid_remote = new_videos.read()
vid_remote = vid_remote.strip().split('\n')

print('Local videos:')
print(vid_local)
print('Remote videos:')
print(vid_remote)

### Define difference sets
difference_add = set(vid_remote) - set(vid_local)
difference_remove = set(vid_local) - set(vid_remote)

#print('Difference to add:')
#print(difference_add)
#print('Difference to remove')
#print(difference_remove)

### Upload new videos
print('Files to be uploaded:')
print(difference_add)

if len(difference_add) >0:	# If there are any files in the remote folder not in the local folder
	for video in difference_add:
		print(video)
#		print('rclone copy test5:/mobile_one/'+ video + ' /home/pi/Rocket-dashboard/Video')
		os.system('rclone copy test5:/mobile_one/'+ video + ' /home/pi/Rocket-dashboard/Videos')
		print(video + ' Uploaded.')

print('Uploads complete')

"""
### Move old videos
if len(difference_remove) >0:
	for video in difference_remove:
		print(video)
		os.system('mv /home/pi/Rocket-dashboard/Videos/' + video + ' /home/pi/Rocket-dashboard/Videos-old')

print('Video transfer complete')
"""
"""
path = "/home/pi/Rocket-dashboard/Sounds"
files_sorted_by_date = []
filepaths = [os.path.join(path, file) for file in os.listdir(path)]
file_statuses = [(os.stat(filepath), filepath) for filepath in filepaths]
files = ((status[stat.ST_CTIME], filepath) for status, filepath in file_statuses if stat.S_ISREG(status[stat.ST_MODE]))


for creation_time, filepath in sorted(files):
    creation_date = time.ctime(creation_time)
    filename = os.path.basename(filepath)
    files_sorted_by_date.append(creation_date + " " + filename)

print(files_sorted_by_date)
"""
