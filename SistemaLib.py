from Estacao import *
from Tempo import *
from DAO import *
from decimal import Decimal
import datetime
import time
#import Listinha


class SistemaLib:
    def __init__(self):
        self.con = dao()
        
    def buscarPorId(self, indice):
        estacao = self.con.buscarPorId(indice)
        return estacao
        
    def listarUltimosMinutos(self, minutos):
        lista = self.con.listarUltimosMinutos(minutos)
        #for i in range(len(lista)):
            #print("ID: {} - Temp1: {} - Temp2: {} - Ultra1: {} - Ultra2: {} - Peso: {} - Data: {} - SValvula: {} - SBomba: {} - Mensagem: {} - CAgua: {} - CAlimento: {}".format(lista[i]._indice, lista[i]._temp1, lista[i]._temp2, lista[i]._ultra1, lista[i]._ultra2, lista[i]._peso, lista[i]._data, lista[i]._statusValvula, lista[i]._statusBomba, lista[i]._mensagem, lista[i]._consumoAgua, lista[i]._consumoAlimento))
        return lista 
        
    def dateTimeSimulator(self, quantidade):
        sistemaLib = SistemaLib()
        listaDateTime = []
        currentDT = datetime.datetime.now()
        tempo = Tempo(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second)
        if tempo._mes < 10:
            tempo._mes = '0' + str(tempo._mes)
        if tempo._dia < 10:
            tempo._dia = '0' + str(tempo._dia)
        if tempo._segundo < 10:
            tempo._segundo = '0' + str(tempo._segundo)
        #print (str(currentDT))
        totalMinutos = int(tempo._hora) * 60 + int(tempo._minuto)
        
        for i  in range(0, quantidade):
            novoTotalMinuto= totalMinutos - i
            hora = int(novoTotalMinuto/60)
            minuto = totalMinutos - (hora*60) - i
            #print(str(hora) + " : " + str(minuto))
            if hora < 10:
                hora = '0' + str(hora)
            if minuto < 10:
                minuto = '0' + str(minuto)
            
            stringDateTime = str(tempo._ano) + '-' + str(tempo._mes) + '-' + str(tempo._dia) + ' ' + str(hora) + ':' + str(minuto) + ':' + str(tempo._segundo)
            #print(stringDateTime)
            listaDateTime.append(stringDateTime)
        for i in range(len(listaDateTime)):
            #print(listaDateTime[i])
            lista = sistemaLib.listarUltimosRegistros(quantidade)
        for i in range(len(lista)):
            #print("ID: {} - Temp1: {} - Temp2: {} - Ultra1: {} - Ultra2: {} - Peso: {} - Data: {} - SValvula: {} - SBomba: {} - Mensagem: {} - CAgua: {} - CAlimento: {}".format(lista[i]._indice, lista[i]._temp1, lista[i]._temp2, lista[i]._ultra1, lista[i]._ultra2, lista[i]._peso, lista[i]._data, lista[i]._statusValvula, lista[i]._statusBomba, lista[i]._mensagem, lista[i]._consumoAgua, lista[i]._consumoAlimento))
            lista[i]._data = listaDateTime[i]
            sistemaLib.atualizarDados(lista[i])
  
    
    def listarUltimosRegistros(self, quantidade):
         lista = self.con.listarUltimosRegistros(quantidade)
         #for i in range(len(lista)):
            #print ('Nome - '  + str(lista[i]._nome)) 
            #print("ID: {} - Temp1: {} - Temp2: {} - Ultra1: {} - Ultra2: {} - Peso: {} - Data: {} - SValvula: {} - SBomba: {} - Mensagem: {} - CAgua: {} - CAlimento: {}".format(lista[i]._indice, lista[i]._temp1, lista[i]._temp2, lista[i]._ultra1, lista[i]._ultra2, lista[i]._peso, lista[i]._data, lista[i]._statusValvula, lista[i]._statusBomba, lista[i]._mensagem, lista[i]._consumoAgua, lista[i]._consumoAlimento))
         return lista
          
    def listar(self):
        lista = self.con.listarDados()
        for i in range(len(lista)):
            #print ('Nome - '  + str(lista[i]._nome)) 
            print("ID: {} - Temp1: {} - Temp2: {} - Ultra1: {} - Ultra2: {} - Peso: {} - Data: {} - SValvula: {} - SBomba: {} - Mensagem: {} - CAgua: {} - CAlimento: {}".format(lista[i]._indice, lista[i]._temp1, lista[i]._temp2, lista[i]._ultra1, lista[i]._ultra2, lista[i]._peso, lista[i]._data, lista[i]._statusValvula, lista[i]._statusBomba, lista[i]._mensagem, lista[i]._consumoAgua, lista[i]._consumoAlimento))
    
    def verificarRegistrosVazios(self, estacao):
        if estacao._ultra2 ==  None:
            print("achado None !!!!!!!!!!!!!!!!!!!!!!!!!!!!")      
    
    def retornaUltimoRegistro(self):
        print("CARREGOU SistemaLIB - RETORNA ULTIMO REGISTRO")
        #estacao = Estacao('','','','','','','','','','','','')
        estacao = self.con.ultimoRegistro()
        #kk.verificarRegistrosVazios(estacao)
        print("Id do ultimo Registro: " + str(estacao._indice))
        '''print("Temp1: " + str(estacao._temp1))
        print("Temp2: " + str(estacao._temp2))
        print("Ultra1: " + str(estacao._ultra1))
        print("Ultra2: " + str(estacao._ultra2))
        print("Peso: " + str(estacao._peso))
        print("Data: " + str(estacao._data.strftime('%Y-%m-%d')))
        print("Hora: " + str(estacao._data.strftime('%H:%M:%S')))
        print("Status Valvula: " + str(estacao._statusValvula))
        print("Status Bomba: " + str(estacao._statusBomba))
        print("Mensagem: " + str(estacao._mensagem))
        print("Consumo Agua: " + str(estacao._consumoAgua))
        print("Consumo Alimento: " + str(estacao._consumoAlimento))
        print(" ------    FIM DO SISTEMA.LIB Retornar ultimo registro   ------")'''
        return estacao
    
    def atualizarDados(self, estacao):
        self.con.atualizarDados(estacao)
        print("Dados atualizados com sucesso")
    
    def gravar(self, estacao):
        self.con.inserirDados(estacao)
        
    def ultimaData(self):
        estacao = self.con.ultimoRegistro()
        data = str(estacao._data.strftime('%Y-%m-%d'))
        return data
    
    def ano(self, estacao):
        ano = str(estacao._data.strftime('%Y'))
        return int(ano)
    
    def mes(self, estacao):
        mes = str(estacao._data.strftime('%m'))
        return int(mes)
    
    def ultimoTempo(self):
        estacao = kk.retornaUltimoRegistro()
        tempo = Tempo(str(estacao._data.strftime('%Y')), str(estacao._data.strftime('%m')), str(estacao._data.strftime('%d')), str(estacao._data.strftime('%H')), str(estacao._data.strftime('%M')), str(estacao._data.strftime('%S')))
        return tempo


#
# BUSCA POR ID
#
#sistemaLib = SistemaLib()
#estacao = sistemaLib.buscarPorId(168)
#print("buscar por id")
#print(estacao._indice)
#print(estacao._ultra1)




#
# LISTAR ULTIMOS MINUTOS
#
#sistemaLib = SistemaLib()
#sistemaLib.listarUltimosMinutos(20)
#
# DATE TIME SIMULATOR
#
#sistemaLib = SistemaLib()
#sistemaLib.dateTimeSimulator()
#
#Listar ULTIMOS REGISTROS
#
#kk = SistemaLib()
#kk.listarUltimosRegistros(4)
#
#RETORNA TEMPO
#
'''kk = Sistema()
print("instanciou Sistema")
tempo = object
tempo = kk.ultimoTempo()
print("retorna ultimo tempo")
print(tempo._mes)
soma = int(tempo._mes) + 30
print(soma)'''


#
#Retorna ANO
#
'''kk= Sistema()
ano = kk.mes(kk.retornaUltimoRegistro())
soma = ano +1
print(soma)'''

#
#ULTIMA DATA
#
'''kk = Sistema()
data=kk.ultimaData()
print("olha a data")
print(data)
print(data[0:4])
print(data[5:7])
num = Decimal(data[5:7])
soma = num + 1
print("resultado")
print(soma)'''

#
#LISTAR DADOS
#
#kk = SistemaLib()
#kk.listar()
#print("Sistema")

#
#ALTERAR TABELA
#
'''kk = Sistema()
estacao = object
estacao = kk.retornaUltimoRegistro()
print("Data Calendario Retornada: " + str(estacao._data.strftime('%Y-%m-%d %H:%M:%$S')))
print("Temp1: " + str(estacao._temp1))
estacao._data = '2018-02-10 17:18:19'
estacao._mensagem = 'Falha'
kk.atualizarDados(estacao)'''

#
#CARREGAR ULTIMO SALVO
#
#kk = SistemaLib()
#kk.retornaUltimoRegistro()

#
#GRAVAR DADOS
#
'''kk = SistemaLib()
estacao = Estacao('','','','','','','','','','','','')
estacao = kk.retornaUltimoRegistro()
print("Data Calendario Retornada: " + str(estacao._data.strftime('%Y-%m-%d %H:%M:%S')))
print("Temp1: " + str(estacao._temp1))
estacao._temp1 = int(46)
estacao._mensagem = 'Falha'
estacao._data = datetime.datetime.now()
kk.gravar(estacao)
estacao = kk.retornaUltimoRegistro()'''
