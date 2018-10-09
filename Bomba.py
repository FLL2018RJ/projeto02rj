import RPi.GPIO as GPIO
#import time
from LedControle import *


class Bomba(object):
    
    def ligaBombaPoco(self):
        led = 36
        pino = 8
        tempoLedLigado = 0.5
        LedControle.acende(led, tempoLedLigado)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pino,GPIO.OUT)
        print('Bomba Poco ON')
        GPIO.output(pino,GPIO.HIGH)
        
    def desligaBombaPoco(self):
        led = 36
        pino = 8
        print('Bomba Poco OFF')
        GPIO.output(pino,GPIO.LOW)
        LedControle.apaga(led)
        
    def ligaBombaBebedouro(self):
        led = 33
        pino = 12
        tempoLedLigado = 0
        LedControle.acende(led, tempoLedLigado)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pino,GPIO.OUT)
        print('Bomba Bebedouro ON')
        GPIO.output(pino,GPIO.HIGH)
        
    def desligaBombaBebedouro(self):
        led = 33
        pino = 12
        print('Bomba Bebedouro OFF')
        #GPIO.setmode(GPIO.BOARD)
        GPIO.output(pino,GPIO.LOW)
        LedControle.apaga(led)
        
