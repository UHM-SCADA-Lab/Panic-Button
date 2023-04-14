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

# global panic bool
status = False


def panic_pressed():
    print("Changing button status")
    global status
    status = not status


def led_control():
    led1 = LED(22)
    led2 = LED(27)
    sleep(3)
    global status
    print("Starting Loop")
    while True:
        if not status:
            led1.off()
            led2.off()
            sleep(33 / 1000)
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
            global status
            panic = status
            print("Panicking!")
            return panic

    api.add_resource(Panic, '/')
    print("app.run next")
    app.run(host=IPAddr)
    print("app running")


if __name__ == "__main__":

    # Testing only
    import urllib.request

    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    print(external_ip)

    print("setting up button")
    button = Button(2)
    button.when_pressed = panic_pressed
    print("button should work")

    # Create threads
    print("Creating LED control thread")
    led_thread = threading.Thread(target=led_control)
    led_thread.setDaemon(True)
    print("Creating API call thread")
    api_thread = threading.Thread(target=apicall)
    api_thread.setDaemon(True)

    # Start threads
    print("starting led control thread")
    led_thread.start()
    print("starting API thread")
    api_thread.start()

    # Wait for threads to complete (they should not)
    led_thread.join()
    api_thread.join()
