import RPi.GPIO as GPIO
import time
from LedControle import *

class Ultrassom(object):
    
    def ultrassomBebedouro(self):
        led = 37
        tempoAcesoLed = 0
        LedControle.acende(led, tempoAcesoLed)
        time.sleep(0.0)
        GPIO.setmode(GPIO.BOARD)
        trig = 11
        echo = 13
        offset = round (0.6, 2)
        try:
            GPIO.setup(trig,GPIO.OUT)
            GPIO.setup(echo,GPIO.IN)
            
            #print('Setup')
            GPIO.output(trig, False)
            time.sleep(1)

            #print('Ping 8x40KHz pulses (trigger)')
            GPIO.output(trig,True)
            time.sleep(0.000001)
            GPIO.output(trig, False)
            
            while GPIO.input(echo)==0:
                pulse_begin = time.time()
            while GPIO.input(echo)==1:
                pulse_end = time.time()
            #print('Reading finished do ultra Bebedouro. Classe ULTRASOM.py')
            pulse_width = pulse_end - pulse_begin

            dist = pulse_width * 17150
            dist = round(dist - offset, 1)
            if dist > 2 and dist < 400:
                LedControle.apaga(led)
                #print("distancia medida do sensor a agua bebedouro", dist)
                #GPIO.cleanup()
                #Subtração para mostrar nivel de agua
                dist = 16 - dist
                #round(dist,2)
                return round(dist,2)
            else:
                print('Out Of Range (2cm - 4m)')
                LedControle.apaga(led)
                dist = 0
                return dist
        except:
            LedControle.apaga(led)
            dist = 0
            return dist    

        #GPIO.cleanup()
        print("Done")
        
         
    def leituraBebedouro(self):
        Ultra = Ultrassom()
        a = Ultra.ultrassomBebedouro()
        print("Bebedouro a: ",a)
        time.sleep(0.3)
        b = Ultra.ultrassomBebedouro()
        print("Bebedouro b: ",b)
        time.sleep(0.3)
        c = Ultra.ultrassomBebedouro()
        print("Bebedouro c: ",c)
        time.sleep(0.3)
        d = Ultra.ultrassomBebedouro()
        print("Bebedouro d: ", d)
        #time.sleep(0.2)
        #e = Ultra.ultrassomBebedouro()
        #print("e: ", e)
        media = (a+b+c+d)/4
        return round(media,0)
    
    
    def ultrassomPoco(self):
        led = 35
        tempoAcesoLed = 0
        LedControle.acende(led, tempoAcesoLed)
        time.sleep(0.0)
        GPIO.setmode(GPIO.BOARD)
        trig = 38
        echo = 40
        offset = round (0.6, 2)
        try:
            GPIO.setup(trig,GPIO.OUT)
            GPIO.setup(echo,GPIO.IN)
            
            #print('Setup')
            GPIO.output(trig, False)
            time.sleep(1)

            #print('Ping 8x40KHz pulses (trigger)')
            GPIO.output(trig,True)
            time.sleep(0.000001)
            GPIO.output(trig, False)
            
            while GPIO.input(echo)==0:
                pulse_begin = time.time()
            while GPIO.input(echo)==1:
                pulse_end = time.time()
            #print('Reading finished')
            pulse_width = pulse_end - pulse_begin

            dist = pulse_width * 17150
            dist = round(dist - offset, 1)
            if dist > 2 and dist < 400:
                LedControle.apaga(led)
                #GPIO.cleanup()
                #Subtração para mostar nivel de água
                dist = 20.5 - dist
                return round(dist, 2)
            else:
                LedControle.apaga(led)
                print('Out Of Range (2cm - 4m)')
                dist = 0
                return dist
        except:
            LedControle.apaga(led)
            dist = 0
            return dist 
            
            #GPIO.cleanup()
        print("Done")
    
    def leituraPoco(self):
        Ultra = Ultrassom()
        a = Ultra.ultrassomPoco()
        print("Poço a: ",a)
        time.sleep(0.3)
        b = Ultra.ultrassomPoco()
        print("Poço b: ",b)
        time.sleep(0.3)
        c = Ultra.ultrassomPoco()
        print("Poço c: ",c)
        time.sleep(0.3)
        d = Ultra.ultrassomPoco()
        print("Poço d: ", d)
        #time.sleep(0.2)
        #e = Ultra.ultrassomPoco()
        #print("e: ", e)
        media = (a+b+c+d)/4
        return round(media,0)