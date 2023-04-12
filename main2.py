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

# global panic
status = False


def panicpressed():
    global status
    status = not status


def ledcontrol():
    led1 = LED("GPIO22")
    led2 = LED("GPIO27")
    while True:
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

    class Panic(Resource):
        def get(self):
            panic = status
            return panic

    api.add_resource(Panic, '/')

    app.run(host='10.1.1.145')


def buttoncontrol():
    button = Button("GPIO15")
    button.when_pressed = panicpressed
    pause()

if __name__ == "__main2__":
    # Create threads
    apithread = threading.Thread(target=apicall(), name='apithread')
    ledthread = threading.Thread(target=ledcontrol(), name='ledthread')
    buttonthread = threading.Thread(target=buttoncontrol(), name='buttonthread')

    # Start threads
    ledthread.start()
    apithread.start()
    buttonthread.start()

    # Wait for threads to complete (they should not)
    ledthread.join()
    apithread.join()
    buttonthread.join()
