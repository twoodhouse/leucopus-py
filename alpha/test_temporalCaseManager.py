#!/usr/bin/python3.5
from temporalCaseManager import TemporalCaseManager
from ioinator import Visinator, Actinator
import requests

requests.get("http://buttonlight01.env:5000/resetall")
visinator = Visinator("http://buttonlight01.env:5000/checklight", [])
actinator = Actinator(["http://buttonlight01.env:5000/pushbutton", "http://buttonlight01.env:5000/resetbutton"])

# tcm = TemporalCaseManager()
