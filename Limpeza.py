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


class Limpeza(object):
    
    def __init__(self):
        print("Limpeza.PY")
        
    def limpa(self, testeSensorPeso):
        print("Dentro do metodo limpa da classe LIMPEZA.PY")
        
        sistemaLib = SistemaLib()
        temp = Temperatura()
        ultra = Ultrassom()
        peso = PesoUnica()
        estacao = Estacao('','','','','','','','','','','','')
        email = EnviaEmail()
        bomba = Bomba()
        alturaBebedouroCheio = 9
        #Mínimo 09 cm de água no Poço(21-12=9) para iniciar a Limpeza
        if ultra.leituraPoco() >= 8:
            print("Entrou na limpeza. leitura do poco: ", ultra.leituraPoco())
            aviso = "Limpeza Iniciada. "
            statusValvula = "Aberta"
            estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), statusValvula, 'Desligada', aviso,'','')
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
            
            #Bebedouro vazio 5 cm de água(25-5=20) 
            if ultra.leituraBebedouro() <= 5:
                print("bebedouro já está vazio. Leitura do bebedouro: ", ultra.leituraBebedouro())
                aviso = aviso + "Bebedouro já está vazio. Ligar Bomba. "
                statusValvula = "Fechada"
                statusBomba = "Ligada"
                estacaoAgora._mensagem = aviso
                estacaoAgora._statusValvula = statusValvula
                estacaoAgora._statusBomba = statusBomba
                sistemaLib.gravar(estacaoAgora)
            else:
                #Temos que esvaziar o Bebedouro
                print("Temos que esvaziar o bebedouro")
                #
                # LIGAMOS A BOMBA PARA ESVAZIAR O BEBEDOURO
                aviso = aviso + "Esvaziando Bebedouro. "
                estacaoAgora._mensagem = aviso
                sistemaLib.gravar(estacaoAgora)
                bomba.ligaBombaBebedouro()
                #Bebdouro vazio tem 5Cm de aǵua (25-5=20)
                while (ultra.leituraBebedouro() > 5):
                    time.sleep(1)
                #Esvaziou bebedouro então fecha a válvula
                bomba.desligaBombaBebedouro()
                #Gravar novos registros após esvaziar o Bebedouro
                aviso = "Bebedouro esvaziado. "
                estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), 'Fechada', 'Ligada', aviso, 0,'')
                estacao = sistemaLib.retornaUltimoRegistro()
                
                #
                #Registros de Consumo novamente. Agua Consumida é ZERO --> Esvaziou o bebedouro.
                if testeSensorPeso == 'erro':
                    alimentoConsumido = 0
                else:
                    alimentoConsumido = estacao._peso - estacaoAgora._peso
                    if alimentoConsumido < 0:
                        alimentoConsumido = 0
            
                    
                estacaoAgora._consumoAlimento = alimentoConsumido        
                
                aviso = aviso + "Enchendo Bebedouro. "
                estacao._mensagem = aviso
                sistemaLib.gravar(estacaoAgora)
            #
            #AQUI MODIFIQUEI MARGEM    
            #Vamos ENCHER BEBEDOURO
            bomba.ligaBombaPoco()
            nivelPoco = 'Cheio'
            while (ultra.leituraBebedouro() < 9):
                if ultra.leituraPoco() < 5:
                    nivelPoco = 'Vazio'
                    break
                time.sleep(0.5)
            #Bebedouro encheu caso o  Poço não tenha ficado vazio  
            if nivelPoco != "Vazio":
                bomba.desligaBombaPoco()
                aviso = "Limpeza terminada. "
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
                aviso = "Limpeza interrompida. Poço vazio. "
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
                    
                #MANDAR EMAIL: POÇO SECOU DURANTE ENCHIMENTO: LIMPEZA INTERROMPIDA
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
        # NÃO HAVERÁ LIMPEZA POS NAO HÁ ÁGUA PARA ISSO
        #
        else:
            aviso = "Limpeza não inicializada. Poço Vazio. "
            statusValvula = "Fechada"
            estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro(), ultra.leituraPoco(),peso.pesa(),datetime.datetime.now(), statusValvula, 'Desligada', aviso, 0,'')
            estacao = sistemaLib.retornaUltimoRegistro()
            print("Limpeza não inicializada. Poço Vazio. ")
            
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