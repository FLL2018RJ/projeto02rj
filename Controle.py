from PesoUnica import *
from Ultrassom import *
from Temperatura import *
#from LedControle import *
#from Bomba import *
from EnviaEmail import *
from SistemaLib import *
from Estacao import *
from Tempo import *
#from random import *
#from Arquivo import *
from Pesagem import *
from Limpeza import *
from TrocaTemperatura import *
from Reabastecimento import *
import time
import datetime


class Controle(object):
    
    def __init__(self):
        print("Controle.PY")
    
    def inicio(self):
        
        sistemaLib = SistemaLib()
        temp = Temperatura()
        ultra = Ultrassom()
        peso = PesoUnica()
        estacao = Estacao('','','','','','','','','','','','')
        email = EnviaEmail()
        arquivos = Arquivos()
        bomba = Bomba()
        pesagem = Pesagem()
        limpeza = Limpeza()
        reabastecimento = Reabastecimento()
        trocaTemperatura = TrocaTemperatura()
        
        
        print("dentro do inicio controle")
        # Análise de erros
        testeSensorPeso = 'ok'
        testeUltra = 'ok'
        testeTermometro = 'ok'
        avisoTeste = ''
        
        #Análise Sensor de Peso
        pesoMaximo = 4
        valorPeso = peso.pesa()
        print("Peso: ", valorPeso)
        if valorPeso < 0 or valorPeso > pesoMaximo:
            avisoTeste = "Erro sensor de peso. "
            testeSensorPeso = 'erro'
        
        #Análise de Sensores de Utrasom
        ultraBebedouro = ultra.leituraBebedouro()
        print("ultra bebedouro: ", ultraBebedouro)
        ultraPoco = ultra.leituraPoco()
        print("ultra poço: ", ultraPoco)
        if ultraBebedouro <= 0 or ultraBebedouro > 16:
            avisoTeste = avisoTeste + "Erro ultrasom bebedouro. "
            testeUltra = 'erro'
        if ultraPoco <= 0 or ultraPoco > 20:
            avisoTeste = avisoTeste + "Erro ultrasom poço. "
            testeUltra = 'erro'
        print("Aviso teste: ", avisoTeste)
        print("Teste ultra: ", testeUltra)
        
        #Análise de Sensores de Temperatura
        tempBebedouro = temp.tempBebedouro()
        tempPoco = temp.tempPoco()
        print("Tem bebedouro: ", tempBebedouro, "  Temp Poco: ", tempPoco)
        if tempBebedouro < 0 or tempBebedouro > 50:
            avisoTeste = avisoTeste + "Erro termômetro bebedouro. "
            testeTermometro = 'erro'
        if tempPoco < 0 or tempPoco > 50:
            avisoTeste = avisoTeste + "Erro termômetro poço. "
            testeTermometro = 'erro'
        print("Aviso Teste Termometro: ", avisoTeste)
        print("Teste termometro: ", testeTermometro)
        
        #Caso todos as leituras dos sensores estejam corretas
        if testeSensorPeso == 'ok' and testeUltra == 'ok' and testeTermometro == 'ok':
            avisoTeste = "Sensores funcionando"
        
        #Gravar dados dos sensores // adicionar mensagens // calcular consumo de alimento e água (colocar ZERO se houver erro) // gravar status
        #Mas antes, analisar Erros para fazer cálculos de consumo
        
        estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),ultra.leituraBebedouro() , ultra.leituraPoco(), peso.pesa(),datetime.datetime.now(), 'Fechada', 'Desligada', avisoTeste, 0,'')
        estacao = sistemaLib.retornaUltimoRegistro()
        print(estacaoAgora._mensagem)
        
        if testeSensorPeso == 'erro':
            alimentoConsumido = 0
        else:
            alimentoConsumido = estacao._peso - estacaoAgora._peso
            if alimentoConsumido < 0:
                alimentoConsumido = 0
                
        estacaoAgora._consumoAlimento = alimentoConsumido        
        
        sistemaLib.gravar(estacaoAgora)
        
        #Manda email porque encontrou erro
        if testeSensorPeso == 'erro' or testeUltra == 'erro' or testeTermometro == 'erro':
            lista = sistemaLib.listarUltimosMinutos(4)
            enviarEmail = 0
            for i in range(len(lista)):
                aviso = avisoTeste
                #Esse condicional IF retorna 0 (que é diferente de -1) caso encontre a mensagem 
                if lista[i]._mensagem.find(aviso) != -1:
                    enviarEmail = enviarEmail + 1
            #Manda email pq só tem uma mensagem de Erro que é a atual. Caso tenha mais de uma é porque já foi enviado anteriormente email        
            if enviarEmail == 1:
                print("Mandou Email")
                email.email(avisoTeste)

        
        #
        # Fim dos Testes
        # Checar Peso
        #
        
        if testeSensorPeso == 'ok':
            print("Sensor de Peso Funcionando. Realizando Pesagem")
            pesagem.checaAlimento(testeUltra)
            
        #
        # Limpeza
        #
        
        if testeUltra == 'ok':
            print("Sensores de ultrassom funcionando. Ira realizar a LIMPEZA se não foi feita nos ultimos minutos")
            #
            #Aqui define o intervalo para realização da Limpeza
            lista = sistemaLib.listarUltimosMinutos(3)
            realizarLimpeza = 0
            for i in range(len(lista)):
                aviso1 = "Limpeza terminada."
                aviso2 = "Troca terminada."
                #Esse condicional IF retorna 0 (que é diferente de -1) caso encontre a mensagem 
                if lista[i]._mensagem.find(aviso1) != -1 or lista[i]._mensagem.find(aviso2) != -1 :
                    realizarLimpeza = realizarLimpeza + 1
            #Realiza limpeza caso não incrementou a variavel "relizarLimpeza". Caso tenha mais de uma é porque já foi enviado anteriormente email        
            if realizarLimpeza == 0:
                print("Faz muito tempo que não há limpeza ou troca de água devido a temperatura. Limpeza será realizada.")
                limpeza.limpa(testeSensorPeso)
            else:
                print("Limpeza ou Troca realizada a pouco tempo. Por isso não será feita.")
        else:
            print("Nao será feita Limpeza porque ultrassom não funciona")
        
        #
        #TrocaTemperatura
        #
        if testeUltra == 'ok' and testeTermometro == 'ok':
            temperaturaMaximaBebedouro = 27
            temperaturaMinimaPoco = 25
            if temp.tempBebedouro() > temperaturaMaximaBebedouro and estacaoAgora._temp2 < temperaturaMinimaPoco:
                print("Sensores de ultrassom funcionando. Temperatura inadequada no bebedouro. Troca será feita caso não haja nenhuma recente.")
                #Aqui define o intervalo para realização da Troca
                lista = sistemaLib.listarUltimosMinutos(1)
                realizarTroca = 0
                for i in range(len(lista)):
                    aviso1 = "Limpeza terminada."
                    aviso2 = "Troca terminada."
                    #Esse condicional IF retorna 0 (que é diferente de -1) caso encontre a mensagem 
                    if lista[i]._mensagem.find(aviso1) != -1 or lista[i]._mensagem.find(aviso2) != -1 :
                        realizarTroca = realizarTroca + 1
                #Realiza troca caso não incrementou a variavel "relizarTroca". Caso tenha mais de uma é porque já foi enviado anteriormente email        
                if realizarTroca == 0:
                    print("Faz muito tempo que não há limpeza ou troca de água devido a temperatura. Troca será realizada.")
                    trocaTemperatura.troca(testeSensorPeso)
                else:
                    print("Troca realizada a pouco tempo. Por isso não será feita.")
            else:
                if estacaoAgora._temp1 < temperaturaMaximaBebedouro:
                    print("Não será feita Troca. Temperatura adequada no bebedouro")
                else:
                    print("Não será feita Troca devido a alta temperatura no poço")
        else:
            if testeUltra != 'ok':
                print("Nao será feita Troca devido a defeito no Ultrassom")
            else:
                print("Nao será feita Troca devido a defeito no Termometro")
                
        #
        #Reabastecimento
        #
        if testeUltra == 'ok':
            print("Verificando nivel de água para reabastecimento")
            if ultra.leituraBebedouro() <= 7:
                reabastecimento.reabastece(testeSensorPeso)
                
        else:
            print("Erro no ultrassom. Reabastecimento não será realizado")
            
controle = Controle()
controle.inicio()
print("fim do Sistema")