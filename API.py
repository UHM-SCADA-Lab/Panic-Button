###API.py
### Date 11-15-22
### Author Bodie Collins
### Function program for Restful API

from flask import Flask, request
from flask_restful import Api, Resource
import RPi.GPIO as GPIO

apiIn = 37

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(apiIn, GPIO.IN)
app = Flask(__name__)
api = Api(app)


class Panic(Resource):
    def get(self):
        panic = GPIO.input(apiIn)
        return panic


api.add_resource(Panic, '/')

if __name__ == "__main__":
    app.run(host='10.1.1.145')
