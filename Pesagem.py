from PesoUnica import *
from Ultrassom import *
from Temperatura import *
from LedControle import *
from EnviaEmail import *
from SistemaLib import *
from Estacao import *
from Tempo import *
from Arquivo import *
import time
import datetime


class Pesagem(object):
    
    def __init__(self):
        print("Pesagem.PY")
    
    def checaAlimento(self, testeUltra):
        sistemaLib = SistemaLib()
        temp = Temperatura()
        ultra = Ultrassom()
        peso = PesoUnica()
        estacao = Estacao('','','','','','','','','','','','')
        email = EnviaEmail()
        arquivos = Arquivos()
        
        print("Dentro do inicio Pesagem")
        estacaoAgora = Estacao('', temp.tempBebedouro(),temp.tempPoco(),round(ultra.leituraBebedouro(),2), round(ultra.leituraPoco(),2),peso.pesa(),datetime.datetime.now(), 'Fechada', 'Desligada', '', 0,'')
        estacao = sistemaLib.retornaUltimoRegistro()

       #Trato dos Consumo de alimento e de água (penultima Leitura - leitura atual = consumo EXCETO se consumo der negativo(pq Houve reabastecimento), então
        # consumo será ZERo, OU se tiver erro no ultrassom (testeUltra = 0), logo consumo de aǵua ZERO)
        alimentoConsumido = estacao._peso - estacaoAgora._peso
        if alimentoConsumido < 0:
            alimentoConsumido = 0
                
        estacaoAgora._consumoAlimento = alimentoConsumido        
        
        aviso = ''
        mandaEmail = 'nao'
        #Checa volume de alimento e manda email se for necessário
        if estacaoAgora._peso > 1.5:
            aviso = "Boa quantidade de Alimento."
        elif estacaoAgora._peso >= 1 and estacaoAgora._peso < 2:
            aviso = "Pouca quantidade de Alimento."
            mandaEmail = 'sim'
        else:
            aviso = "Não há Alimento."
            mandaEmail = 'sim'
        
        estacaoAgora._mensagem = aviso
        print("Mensagem da classe PESAGEM.PY: ", estacaoAgora._mensagem)
        
        sistemaLib.gravar(estacaoAgora)
        
        #
        #manda email porque tem pouco ou nenhum alimento
        #
        if mandaEmail == 'sim':
            #
            #Ajusta o intervalo de tempo para o email
            #
            lista = sistemaLib.listarUltimosMinutos(1)
            enviarEmail = 0
            for i in range(len(lista)):
                aviso = aviso
                #Esse condicional IF retorna 0 (que é diferente de -1) caso encontre a mensagem- Pelo menos uma mensagem ele encontra que foi a condicação
                #para chamar a funcao manda email. Se encontrar só uma, então tem que mandar email
                if lista[i]._mensagem.find(aviso) != -1:
                    enviarEmail = enviarEmail + 1
            #Manda email pq só tem uma mensagem de Erro que é a atual. Caso tenha mais de uma é porque já foi enviado anteriormente email        
            if enviarEmail == 1:
                print("Mandou EMail")
                email.email(aviso)

            
            
            

        
        
        
        
        
    