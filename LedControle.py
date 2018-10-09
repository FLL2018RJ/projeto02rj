import RPi.GPIO as GPIO
import time

class LedControle(object):
    
        def acende(pino, tempoAcesoLed):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(pino,GPIO.OUT)
            GPIO.output(pino,GPIO.HIGH)
            #print('LED ON')
            time.sleep(tempoAcesoLed)
        
        def apaga(pino):
            #print('LED OFF')
            GPIO.output(pino,GPIO.LOW)
            
            