from PesoUnica import *
from Ultrassom import *
from Temperatura import *
from LedControle import *
from Bomba import *
from EnviaEmail import *
from SistemaLib import *
from Estacao import *
import time
import datetime


class Reabastecimento(object):
    
    def __init__(self):
        print("Reabastecimento.PY")
        
    def reabastece(self, testeSensorPeso):
        print("Dentro do metodo reabastece da classe REABASTECIMENTO.PY")
        
        sistemaLib = SistemaLib()
        temp = Temperatura()
        ultra = Ultrassom()
        peso = PesoUnica()
        estacao = Estacao('','','','','','','','','','','','')
        email = EnviaEmail()
        bomba = Bomba()
        alturaBebedouroCheio = 9

     
        if ultra.leituraPoco() > 6:
            print("Entrou no Reabastecimento.")
            aviso = "Reabastecimento Iniciado. Ligar Bomba do Poço."
            estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), 'Fechada', 'Ligada', aviso,'','')
            estacao = sistemaLib.retornaUltimoRegistro()

            #Tratar os registros de consumo
            if testeSensorPeso == 'erro':
                alimentoConsumido = 0
            else:
                alimentoConsumido = estacao._peso - estacaoAgora._peso
                if alimentoConsumido < 0:
                    alimentoConsumido = 0
            
            aguaConsumida =  alturaBebedouroCheio - round(estacaoAgora._ultra1,2)
            if aguaConsumida < 0:
                aguaConsumida = 0
            else:
                unidadeParaVolume = 0.346
                aguaConsumida = aguaConsumida * unidadeParaVolume
                    
            estacaoAgora._consumoAlimento = alimentoConsumido        
            estacaoAgora._consumoAgua = round(aguaConsumida,2)
            
            sistemaLib.gravar(estacaoAgora) 
                   
            #Vamos encher o Bebedouro
            bomba.ligaBombaPoco()
            nivelPoco = 'Cheio'
            #Bebedouro Cheio tem 13cm (25-13=12)
            while (ultra.leituraBebedouro() < 9):
                print("Leitura do bebedouro durante Reabastecimento. Deve parar quando >=9: ", ultra.leituraBebedouro())
                #Poço vazio 4cm (21-4= 17
                if ultra.leituraPoco() < 5:
                    nivelPoco = 'Vazio'
                    break
                time.sleep(0.5)
            #Bebedouro encheu caso o  Poço não tenha ficado vazio  
            if nivelPoco != "Vazio":
                bomba.desligaBombaPoco()
                aviso = "Reabastecimento terminado. "
                estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), 'Fechada', 'Desligada', aviso, 0,'')
                estacao = sistemaLib.retornaUltimoRegistro()
                    
                #Registro de consumo. Agua = ZERO porque o bebedouro encheu
                if testeSensorPeso == 'erro':
                    alimentoConsumido = 0
                else:
                    alimentoConsumido = estacao._peso - estacaoAgora._peso
                if alimentoConsumido < 0:
                    alimentoConsumido = 0
                        
                estacaoAgora._consumoAlimento = alimentoConsumido        
                    
                sistemaLib.gravar(estacaoAgora)
                
            # PAUSA PARA ANALISE    
            #Poço ficou seco durante enchimento. Consumode de água ZERO. Registrar Dados e mandar email
            else:
                bomba.desligaBombaPoco()
                aviso = "Reabastecimento interrompido. Poço vazio. "
                estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), 'Fechada', 'Desligada', aviso, 0,'')
                estacao = sistemaLib.retornaUltimoRegistro()
                    
                #Registro de consumo. Agua = ZERO porque o bebedouro encheu
                if testeSensorPeso == 'erro':
                    alimentoConsumido = 0
                else:
                    alimentoConsumido = estacao._peso - estacaoAgora._peso
                if alimentoConsumido < 0:
                    alimentoConsumido = 0
                        
                estacaoAgora._consumoAlimento = alimentoConsumido        
                    
                sistemaLib.gravar(estacaoAgora)
                    
                #MANDAR EMAIL: POÇO SECOU DURANTE ENCHIMENTO: REABASTECIMENTO INTERROMPIDO
                lista = sistemaLib.listarUltimosMinutos(1)
                enviarEmail = 0
                for i in range(len(lista)):
                    #Esse condicional IF retorna 0 (que é diferente de -1) caso encontre a mensagem 
                    if lista[i]._mensagem.find(aviso) != -1:
                        enviarEmail = enviarEmail + 1
                #Manda email pq só tem uma mensagem de Erro que é a atual. Caso tenha mais de uma é porque já foi enviado anteriormente email        
                if enviarEmail == 1:
                    print("Manda Email porque só tem um unico registro no intervalo de tempo: ", aviso)
                    email.email(aviso)
            
            
                     
         
        #
        # NÃO HAVERÁ REABASTECIMENTO POS NAO HÁ ÁGUA PARA ISSO
        #
        else:
            aviso = "Reabastecimento não inicializado. Pouca água no poço. "
            statusValvula = "Fechada"
            estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), statusValvula, 'Desligada', aviso, 0,'')
            estacao = sistemaLib.retornaUltimoRegistro()
            
            #Tratar do Consumo
            if testeSensorPeso == 'erro':
                alimentoConsumido = 0
            else:
                alimentoConsumido = estacao._peso - estacaoAgora._peso
                if alimentoConsumido < 0:
                    alimentoConsumido = 0
                    
            estacaoAgora._consumoAlimento = alimentoConsumido        
            
            sistemaLib.gravar(estacaoAgora)
            #
            #Manda email porque o poço está vazio
            #
            lista = sistemaLib.listarUltimosMinutos(1)
            enviarEmail = 0
            for i in range(len(lista)):
                #Esse condicional IF retorna 0 (que é diferente de -1) caso encontre a mensagem 
                if lista[i]._mensagem.find(aviso) != -1:
                    enviarEmail = enviarEmail + 1
            #Manda email pq só tem uma mensagem de Erro que é a atual. Caso tenha mais de uma é porque já foi enviado anteriormente email        
            if enviarEmail == 1:
                print("Manda Email porque só tem um unico registro no intervalo de tempo.")
                email.email(aviso)
                
# valorTestePeso = 'ok'            
#kk = Limpeza()
#kk.limpa(valorTestePeso)
