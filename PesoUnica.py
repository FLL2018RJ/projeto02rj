import RPi.GPIO as GPIO
import time
import sys
from LedControle import *
from hx711 import HX711

class PesoUnica(object):
    def pesa(self):
        led = 21
        tempoAcesoLed = 0
        LedControle.acende(led, tempoAcesoLed)
        hx = HX711(29, 31)
        #hx = HX711(5, 6)
        hx.set_reading_format("LSB", "MSB")
        hx.set_reference_unit(-46)

        hx.reset()
        hx.tare()
        
        
        try:
            val = hx.get_weight(5)
            valInteiro = int(val)
            print ("Valor pego pelo sensor de Peso: ", valInteiro)
            print("-------------------")

            hx.power_down()
            hx.power_up()
            time.sleep(0.5)
            LedControle.apaga(led)
            #Determina quanto vale meio Quilo
            unidadeMeioQuilo = 180
            valInteiro = ((int(float(valInteiro/unidadeMeioQuilo))) * 500) /1000
            if valInteiro < 0:
                valInteiro = 0
            return(valInteiro)
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
        
    def cleanAndExit():
        print ("Erro sensor de peso!! GPIO.cleanup")
        GPIO.cleanup()
        #print ("Bye!")
        sys.exit()

