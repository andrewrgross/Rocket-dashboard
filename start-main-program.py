### start-main-program.py -- Andrew R Gross -- 2020-12-21

### Header
import os
import sys
import time

print('Wait ' + sys.argv[1])
time.sleep(float(sys.argv[1]))

os.system('DISPLAY=:0 python3 /home/pi/Rocket-dashboard/main_program_v4.py')
print('Start process complete')
