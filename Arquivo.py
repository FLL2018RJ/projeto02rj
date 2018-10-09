import os

class Arquivos(object):
    
    def primeiraVez():
        with open("ArquivoPrimeiraVez.txt", "r+") as fp:
            line = fp.readline()
            print ('linha :  ')
            print (line)      
            if line == str(1):
                print ('Linha igual a 1 --> Sim eh a primeira vez!!!!')
                os.remove('ArquivoPrimeiraVez.txt')
                fp.close()
                file = open('ArquivoPrimeiraVez.txt', 'w+')
                file.write('0')
                file.close()
                um = 1
                return um
            else:
                print ('Linha igual a 0 --> tem que subtrair o peso da tara')
                fp.close()
                zerao = 0
                return zerao
            
    def gravaTara(tara):
        os.remove('taraInicial.txt')
        file = open('taraInicial.txt', 'w+')
        file.write(str(tara))
        file.close
        print ('Gravou Tara')
            
    def leiaTara():
        file = open('taraInicial.txt', 'r+')
        line = file.readline()
        return line

    def gravaTempoAlimento(minutos):
        os.remove('TempoAlimento.txt')
        file = open('TempoAlimento.txt', 'w+')
        file.write(str(minutos))
        file.close
        print ('Gravou Tempo de Alimento')
        
    def leiaTempoAlimento():
        file = open('TempoAlimento.txt', 'r+')
        line = file.readline()
        return line