##Title: Panic Button Main
##Author: Bodie Collins, Joshua Brewer
##Date: 04-06-23
##Function: To create a functional panic button for UH's SCADA Lab
## This should be much simpler

import threading
from gpiozero import Button, LED  # import Button to press, and LED to control LED
from time import sleep  # import sleep function for LED blinking
import os
from flask import Flask, request
from flask_restful import Api, Resource
from signal import pause
import socket

# global panic
status = False


def panic_pressed():
    global status
    status = not status


def led_control():
    led1 = LED(22)
    led2 = LED(27)
    while True:
        print("LOOP")
        if not status:
            led1.off()
            led2.off()
        elif status:
            led1.on()
            sleep(0.5)
            led1.off()
            led2.on()
            sleep(0.5)
            led2.off()


def apicall():
    app = Flask(__name__)
    api = Api(app)
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("IP Address = " + IPAddr)

    class Panic(Resource):
        def get(self):
            panic = status
            return panic

    api.add_resource(Panic, '/')

    app.run(host=IPAddr)


def button_control():
    button = Button(15)
    button.when_pressed = panic_pressed

    pause()


if __name__ == "__main__":
    # Create threads
    #apithread = threading.Thread(target=apicall(), name='apithread')
    ledthread = threading.Thread(target=led_control(), name='ledthread')
    buttonthread = threading.Thread(target=button_control(), name='buttonthread')

    # Start threads
    buttonthread.start()
    ledthread.start()
    #apithread.start()

    # Wait for threads to complete (they should not)
    buttonthread.join()
    ledthread.join()
    #apithread.join()
