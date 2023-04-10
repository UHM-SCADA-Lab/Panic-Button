##Title: Panic Button Main
##Author: Bodie Collins
##Date: 10-26-22
##Function: To create a functional panic button for UH's SCADA Lab

import RPi.GPIO as GPIO     #import Raspberry PI Library
import time                 #import sleep function for LED blinking
import os

button = 10                 #Set variable for button pin
led1 = 13                   #Set variable for led 1 pin
led2 = 15                   #Set variable for led 2 pin
apiOut = 29                 #Set variable for api panic status
Status = False              #Set variable for status of panic button
buttonStatus = False
oldflash = time.time()
out = True

GPIO.setwarnings(False)     #Ignore Warnings
GPIO.setmode(GPIO.BOARD)    #use physical pin numbering
GPIO.setup(led1, GPIO.OUT, initial=GPIO.LOW)    #Setting pin 13 as an output for led initialize it off
GPIO.setup(led2, GPIO.OUT, initial=GPIO.LOW)    #Setting pin 15 as an output for led2 initialize it off
GPIO.setup(button, GPIO.IN)                     #Setting pin 10 as an input from button
GPIO.setup(apiOut, GPIO.OUT, initial=GPIO.LOW)  #Setting pin 29 as output fro api panic status

#if __name__ == "__main__":
    try:
        while True:                             #Runs forever

            old_button_status = buttonStatus
            buttonStatus = GPIO.input(button)

            if not buttonStatus:
                # Don't want to change the output when button goes from 1->0
                if buttonStatus != old_button_status:
                    # runs when button goes from 0->1
                    Status = not Status
                    GPIO.output(apiOut, Status)

            if not Status:
                GPIO.output(led1,0)
                GPIO.output(led2,0)
            elif Status:
                flash = time.time()
                #flash Leds
                if flash - oldflash > .5:
                    out = not out
                    oldflash = time.time()
                    GPIO.output(led2,out)
                    GPIO.output(led1,not out)
