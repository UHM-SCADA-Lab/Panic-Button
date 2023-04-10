##Title: Panic Button Main
##Author: Bodie Collins, Joshua Brewer
##Date: 04-06-23
##Function: To create a functional panic button for UH's SCADA Lab

import threading
import RPi.GPIO as GPIO  # import Raspberry PI Library

import time  # import sleep function for LED blinking
import os
from flask import Flask, request
from flask_restful import Api, Resource

def