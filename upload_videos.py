### upload_videos.py -- Andrew R Gross -- 2020-12-19

### Header
import os
import stat
import time

### Main program

print('Checking for new videos')
## List local videos

vid_local = os.listdir('/home/pi/Rocket-dashboard/Videos/')

os.system('rclone lsf test5:/mobile_one/>/home/pi/Rocket-dashboard/new_videos')

new_videos = open('/home/pi/Rocket-dashboard/new_videos','r')
vid_remote = new_videos.read()
vid_remote = vid_remote.strip().split('\n')
print(vid_remote)


print('Local videos:')
print(vid_local)
print('Remote videos:')
print(vid_remote)

difference = set(vid_remote) - set(vid_local)

print('Files to be uploaded')
print(difference)

if len(difference) >0:	# If there are any files in the remote folder not in the local folder
	for video in difference:
		print(video)
#		print('rclone copy test5:/mobile_one/'+ video + ' /home/pi/Rocket-dashboard/Video')
		os.system('rclone copy test5:/mobile_one/'+ video + ' /home/pi/Rocket-dashboard/Videos')
		print(video + ' Uploaded.')

print('Uploads complete')

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
