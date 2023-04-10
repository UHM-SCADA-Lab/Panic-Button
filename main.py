##Title: Panic Button Main
##Author: Bodie Collins, Joshua Brewer
##Date: 04-06-23
##Function: To create a functional panic button for UH's SCADA Lab

import threading
import RPI.GPIO as GPIO  # import Raspberry PI Library
import time  # import sleep function for LED blinking
import os
from flask import Flask, request
from flask_restful import Api, Resource

# global bool
isPressed = False


def ledcontrol():
    button = 10  # Set variable for button pin
    led1 = 13  # Set variable for led 1 pin
    led2 = 15  # Set variable for led 2 pin
    status = False  # Set variable for status of panic button
    buttonstatus = False
    oldflash = time.time()
    out = True

    GPIO.setwarnings(False)  # Ignore Warnings
    GPIO.setmode(GPIO.BOARD)  # use physical pin numbering
    GPIO.setup(led1, GPIO.OUT, initial=GPIO.LOW)  # Setting pin 13 as an output for led initialize it off
    GPIO.setup(led2, GPIO.OUT, initial=GPIO.LOW)  # Setting pin 15 as an output for led2 initialize it off
    GPIO.setup(button, GPIO.IN)  # Setting pin 10 as an input from button

    try:
        while True:  # Runs forever

            old_button_status = buttonstatus
            buttonstatus = GPIO.input(button)

            if not buttonstatus:
                # Don't want to change the output when button goes from 1->0
                if buttonstatus != old_button_status:
                    # runs when button goes from 0->1
                    status = not status
                    global isPressed
                    isPressed = status

            if not status:
                GPIO.output(led1, 0)
                GPIO.output(led2, 0)
            elif status:
                flash = time.time()
                # flash Leds
                if flash - oldflash > .5:
                    out = not out
                    oldflash = time.time()
                    GPIO.output(led2, out)
                    GPIO.output(led1, not out)


def apicall():
    app = Flask(__name__)
    api = Api(app)

    class Panic(Resource):
        def get(self):
            panic = isPressed
            return panic

    api.add_resource(Panic, '/')

    app.run(host='10.1.1.145')


if __name__ == "__main__":
    # Create threads
    t1 = threading.Thread(target=ledcontrol(), name='t1')
    print("started Thread t1")
    t2 = threading.Thread(target=apicall(), name='t2')
    print("started Thread t2")

    # Start threads
    t1.start()
    t2.start()

    #Wait for threads to finish. (they should not)
    t1.join()
    t2.join()

    #print if threads finish, should not occur
    print("threads finished")