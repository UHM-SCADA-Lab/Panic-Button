##Title: Panic Button Main
##Author: Bodie Collins, Joshua Brewer
##Date: 04-06-23
##Function: To create a functional panic button for UH's SCADA Lab
## This should be much simpler

import socket
import threading
from time import sleep  # import sleep function for LED blinking
from flask import Flask
from flask_restful import Api, Resource
from gpiozero import Button, LED  # import Button to press, and LED to control LED
import os

# global panic bool
status = False


# return the ip address of the local network excluding the loopback address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# Change state of global bool status
def panic_pressed():
    global status
    status = not status


# Function led_control controls the LEDs
def led_control():
    led1 = LED(22)  # led1 is connected to GPIO 22
    led2 = LED(27)  # led2 is connected to GPIO 27
    global status
    while True:
        if not status:  # Turn both leds off
            led1.off()
            led2.off()
            sleep(33 / 1000)    # check 30 times a second
        elif status:    # Blink leds
            led1.on()
            sleep(0.5)
            led1.off()
            led2.on()
            sleep(0.5)
            led2.off()


def apicall():
    app = Flask(__name__)
    import logging  # Next 4 lines used to suppress the api output
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.logger.disabled = True
    log.disabled = True
    api = Api(app)

    class Panic(Resource):
        def get(self):
            global status
            panic = status
            return panic

    api.add_resource(Panic, '/')
    app.run(host=get_ip())  # start the restful api


if __name__ == "__main__":
    button = Button(2)  # button is connected to GPIO 2
    button.when_pressed = panic_pressed # Creates callback to panic_pressed function

    # Create threads
    led_thread = threading.Thread(target=led_control)   # Create thread that executes led_control()
    api_thread = threading.Thread(target=apicall)   # Create thread that executes apicall()

    # Set threads to be run in background
    led_thread.setDaemon(True)
    api_thread.setDaemon(True)

    # Start threads
    led_thread.start()
    api_thread.start()

    # Wait for threads to complete (they should not)
    led_thread.join()
    api_thread.join()
