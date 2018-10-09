import mysql.connector
from mysql.connector import errorcode
from Estacao import *

class dao:
    def __init__(self):
        try:    
            self.con = mysql.connector.connect(user='root', password='1234', host='localhost', database='db_estacao')
        except mysql.connector.Error as erro:
            if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Usuário/Senha do banco MySql errado(s)")
            elif erro.errno == errorcode.ER_BAD_DB_ERROR:
                print("Banco de Dados inexistente!")
            else:
                print(erro)
        else:
            #print("Conexão feita com sucesso!")
            self.con.close
    
    def buscarPorId (self, indice):
            try:
                dadoDesejado = object
                print ("indice recebido em DAO em BUSCA POR ID")
                indice = str(indice)
                print(indice)
                query = ("select * from estacao where id = %(indiceDesejado)s")
                #query = ("select * from estacao where id = 166")                 
                print("montou a query")
                cursor = self.con.cursor()
                print("criou o cursor")
                cursor.execute(query, {'indiceDesejado': indice })
                #cursor.execute(query)
                #print("executou a query")
                for (id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento) in cursor:
                    dadoDesejado = Estacao(id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento)
                cursor.close()
                #print("dado desejado")
                #print(dadoDesejado._id)  SEMPRE DA ERRO SE COLOCAR ESSA LINHA
            except BaseException as os:
                print("Erro no DAO buscar Por ID")
                return False
            return dadoDesejado
    
    def listarUltimosMinutos (self, minutos):
            try:
                lista = []
                query = ("select * from estacao where datetime between date_sub(now(), interval %(quantidadeMinutos)s minute) and now()")
                cursor = self.con.cursor()
                cursor.execute(query, {'quantidadeMinutos': minutos })
                for (id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento) in cursor:
                    novo = Estacao(id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento)
                    lista.append(novo)
                cursor.close()
            except BaseException as os:
                print("Erro no DAO listar Ultimos Minutos")
                return False
            return lista
    
    def listarUltimosRegistros (self, quantidade):
        try:
            lista = []
            query = ("select * from estacao order by id desc limit %(quantidadeQuerys)s")
            cursor = self.con.cursor() 
            cursor.execute(query, {'quantidadeQuerys': quantidade })
            for (id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento) in cursor:
                novo = Estacao(id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento)
                lista.append(novo)
            cursor.close()
        except BaseException as os:
            print("Erro no DAO listar Ultimos Registros")
            return False
        return lista
            
    def listarDados(self):
        try:
            lista = []
            cursor = self.con.cursor()
            cursor.execute("select * from estacao")
            for (id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento) in cursor:
                novo = Estacao(id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento)
                lista.append(novo)
            cursor.close()
        except BaseException as os:
            print("Erro no DAO de Listar Dados")
            return False
        return lista
    
    def atualizarDados(self,estacao):
        try:
            cursor = self.con.cursor()
            comando = ("UPDATE estacao SET temp1 = %s, temp2 = %s, ultra1 = %s, ultra2 = %s, peso = %s, datetime = %s, status_valvula = %s, status_bomba = %s, mensagem = %s, consumo_agua = %s, consumo_alimento = %s WHERE id = %s")
            print("MONTOU QUERY DAO de atuazalizar Dados")
            print(estacao._mensagem)
            print(estacao._indice)
            valores = (estacao._temp1, estacao._temp2, estacao._ultra1, estacao._ultra2, estacao._peso, estacao._data, estacao._statusValvula, estacao._statusBomba, estacao._mensagem, estacao._consumoAgua, estacao._consumoAlimento, estacao._indice)
            cursor.execute(comando, valores)
            self.con.commit()
            #print("dentro atualizarDAO")
            cursor.close()
            #print("cursor close em atualizar DAO")
        except BaseException as os:
            print("Erro no DAO atualizar")
            return False
        return True
    
    def ultimoRegistro(self):
        try:
            print("CARREGOU DAO.py - ultimo registro")
            ultimoDado = object
            cursor = self.con.cursor()
            print("DAO.py - proximo passo montar query e executa-la")
            cursor.execute("select * from estacao order by id desc limit 1")
            print("DAO.py - Query executado com sucesso")
            for (id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento) in cursor:
                ultimoDado = Estacao(id, temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento)
            cursor.close()
            #self.con.close()
        except BaseException as os:
            print("DAO.py ERRO no retorno do Ultimo Registro")
            return False
        return ultimoDado
    
    def inserirDados(self, estacao):
        try:
            #print("Try inserir Dados")
            cursor = self.con.cursor()
            comando = ("INSERT INTO estacao (temp1, temp2, ultra1, ultra2, peso, datetime, status_valvula, status_bomba, mensagem, consumo_agua, consumo_alimento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            print("DAO.py - Montou Query")
            valores = (estacao._temp1, estacao._temp2, estacao._ultra1, estacao._ultra2, estacao._peso, estacao._data, estacao._statusValvula, estacao._statusBomba, estacao._mensagem, estacao._consumoAgua, estacao._consumoAlimento)
            #print("Pegou Valores")
            cursor.execute(comando, valores)
            #print("Executou o cursor.execute")
            self.con.commit()
            cursor.close()
        except BaseException as os:
            print("DAO.py Erro Exception no DAO em inserir")
            return False
        print("DAO.py - Gravou com sucesso DAO")
        #return ultimo