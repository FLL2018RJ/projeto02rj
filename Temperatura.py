import time
from LedControle import *
import RPi.GPIO as GPIO

class Temperatura(object):
    
    def tempPoco(self):
        led = 23
        tempoAcesoLed = 0
        LedControle.acende(led, tempoAcesoLed)
        tempfile = open("/sys/bus/w1/devices/28-0516702d13ff/w1_slave")
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        temperature = float(tempdata[2:])
        temperature = temperature / 1000
        LedControle.apaga(led)
        return round(temperature,0)

    def tempBebedouro(self):
        led = 32
        tempoAcesoLed = 0
        LedControle.acende(led, tempoAcesoLed)
        tempfile = open("/sys/bus/w1/devices/28-0516702b49ff/w1_slave")
        thetext = tempfile.read()
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        temperature = float(tempdata[2:])
        temperature = temperature / 1000
        LedControle.apaga(led)
        return round(temperature,0)
        