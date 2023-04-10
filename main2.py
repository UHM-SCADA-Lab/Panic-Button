##Title: Panic Button Main
##Author: Bodie Collins, Joshua Brewer
##Date: 04-06-23
##Function: To create a functional panic button for UH's SCADA Lab
## This should be much simpler

import threading
from gpiozero import Button, LED  # import Button to press, and LED to control LED

import time  # import sleep function for LED blinking
import os
from flask import Flask, request
from flask_restful import Api, Resource

# global panic
static = False


def panicpressed():
    global static
    static = not static


def apicall():
    app = Flask(__name__)
    api = Api(app)

    class Panic(Resource):
        def get(self):
            panic = static
            return panic

    api.add_resource(Panic, '/')

    app.run(host='10.1.1.145')
