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


if __name__ == "__main2__":
    button = Button("GPIO15")
    led1 = LED("GPIO22")
    led2 = LED("GPIO27")

    apithread = threading.Thread(target=apicall(), name='apithread')
    ledthread = threading.Thread(target=ledcontrol(), name='ledthread')
    ledthread.start()
    apithread.start()

    button.when_pressed = panicpressed
    pause()
    ledthread.join()
    apithread.join()
