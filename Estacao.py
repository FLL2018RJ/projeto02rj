import time
import datetime

class Estacao(object):
    def __init__(self, indice, temp1, temp2, ultra1, ultra2, peso, data, statusValvula, statusBomba, mensagem, consumoAgua, consumoAlimento):
        #f = '%Y-%m-%d %H:%M:%$S'
        self._indice=indice
        self._temp1=temp1
        self._temp2=temp2
        self._ultra1=ultra1
        self._ultra2=ultra2
        self._peso=peso
        self._data=data
        self._statusValvula=statusValvula
        self._statusBomba=statusBomba
        self._mensagem=mensagem
        self._consumoAgua=consumoAgua
        self._consumoAlimento=consumoAlimento
        
        
#print("Model Estacao")