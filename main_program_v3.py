### main_program_v3.py -- 12-02-2020 -- Andrew R Gross

### Libraries
import pygame
import time
import cv2
import RPi.GPIO as GPIO


pygame.init()
screen = pygame.display.set_mode([500, 500])
screen.fill((255, 255, 255))
# Draw a solid blue circle in the center
pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
### Declare variables and assets

## Images
menucontrol = pygame
## Sounds

## Videos

## Pins
button1
button2
button3
button4
switch1
switch2

## LEDs
led1 = 17
led2 = 1
led3 = 1
led4 = 1

GPIO.setup(button1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led1,GPIO.OUT)

screenstate = 0

switch1status = True
switch2status = True
light1color = (230,240,230)
light2color = (230,230,240)
light3color = (240,230,230)
switch1_color = (235,182,219)

window_list = (win_orbit, win_mars, win_space, win_hole, win_vents)
current_window = 1
# 
print('Setup complete. Running test')

try:
        while True:
#               time.sleep(0.1)
                ### Button1: Select
                if GPIO.input(button1) == False:



# Import and initialize the pygame library

# Set up the drawing window

# Run until the user asks to quit
running = True

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the background with white
    screen.fill((255, 255, 255))
    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    # Flip the display
    pygame.display.flip()
# Done! Time to quit.

pygame.quit()

