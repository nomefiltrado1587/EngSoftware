from operations import Operations
from busca import Busca
from fakeReq import fRequest
import json
from pymysql import Error

class Insercao(Operations):
    
    def _init_(self, mysql):
        return super().__init__(mysql)

    def execute(self, request):
        self.abrirCursor()
        self.accessData(request)
        #keys = self.data.keys()
        #table = list(keys)[0]
        result = self.insertComBusca(request)
        self.fecharCursor()
        return {"created_id": result}

    def gerarQuery(self, data=None):
        if data == None:
            data = self.data
        tName = list(data.keys())[0]
        insert = f"""INSERT INTO {tName} ("""
        values = f""" VALUES("""
        dicio = data[tName]
        for key in dicio:
            if dicio[key] != 'NULL':
                insert += key + ", "
                values += str(dicio[key]) + ", "

        insert = insert[:-2] + ") "
        values = values[:-2] + ");"
        return insert + values        

    def insertIntoTable(self, data=None):
        if data == None:
            data = self.data

        self.cursor.execute(self.gerarQuery(data))
        return self.cursor.lastrowid

    def insertComBusca(self, request):
        exceptions = ["Sediar", "Pacotes"]
        chaves = {
            "Locais": {
                "principal": "local_id",
                "estrangeira": "add_id"
            },
            "Eventos": {
                "principal": "event_id",
                "estrangeira": "details_id"
            },
            "Pacotes": {
                "principal": "pack_id"
            },
            "Det_eventos": {
                "principal": "details_id"
            },
            "Enderecos": {
                "principal": "add_id"
            },
            "Sediar": {
                "principal": "sed_id"
            }
        }
        busca = Busca(self.mysql)
        result = busca.execute(request)
        rowsTable1 = result
        tables = self.separarEntradaGeral(request.json)
        tList = list(tables.keys())
        princ = chaves[tList[0]]["principal"]
        princT1 = tList[0] + "." + princ
        fTables = self.separarEntradaGeral(self.data)
        if len(result) == 0:
            # Caso a busca geral com todos os campos necessários não encontre um resultado
            if len(tList) > 1:
                # Caso haja mais de uma tabela envolvida na inserção (buscas em locais e eventos)
                estr = chaves[tList[0]]["estrangeira"]
                estrT = tList[0] + "." + estr # FIXME - Remover se desnecessário
                request2 = fRequest({tList[1]: tables[tList[1]]})
                rowsTable2 = busca.execute(request2)
                if len(rowsTable2) == 0:
                    # Caso não exista uma linha na tabela "apontada" (Enderecos ou Det_eventos)
                    # com os campos identicamente preenchidos - cria uma linha nova 
                    estId = str(self.insertIntoTable({tList[1]: fTables[tList[1]]}))
                else:
                    # Caso já exista: pega a chave principal dela na tabela
                    princT2 = tList[1] + "." + estr
                    estId = str(rowsTable2[0][princT2])
                fTables[tList[0]][estr] = estId
                reqBody = {estr: str(estId)}
                request3 = fRequest({tList[0]: reqBody})
            if len(rowsTable1) == 0:
                if tList[0] not in exceptions:
                    reqBody = {"nome": tables[tList[0]]["nome"]}
                    request4 = fRequest({tList[0]: reqBody})
                    rowsTable1 = busca.execute(request4)
                if len(rowsTable1) == 0:
                    # Caso não tenha nenhum item encontrado cumprindo todos os requisitos de busca
                    # Cria um novo
                    # Retorna o id do item criado
                    retId = self.insertIntoTable({tList[0]: fTables[tList[0]]})
                else:
                    # Caso já tenha um item na tabela com o mesmo nome do que estão tentando criar
                    # Local ou Evento
                    retId = -2
            else:
                # Caso já tenha um Endereço ou Det_evento idêntico ao pedido para criar, mas que esteja ocupado
                # com outro correspondente (sendo apontado por um Local ou Evento)
                retId = -1
        else:
            # Caso já seja encontrada uma linha com todos os campos identicamente preenchidos na busca completa
            # Retorna o id da linha existente
            retId = result[0][princT1]
        self.connection.commit()
        return retId

    def separarEntradaGeral(self, entrada):
        tratada = {}
        for dicio in entrada:
            match dicio:
                case "evento":
                    dicios = self.dividir_dicts(entrada[dicio], ["nome"])
                    tratada["Eventos"] = dicios[1]
                    tratada["Det_eventos"] = dicios[0]
                case "local":
                    dicios = self.dividir_dicts(entrada[dicio], ["nome"])
                    tratada["Locais"] = dicios[1]
                    tratada["Enderecos"] = dicios[0]
                case "pacote":
                    tratada["Pacotes"] = entrada["pacote"]
                case _:
                    tratada[dicio] = entrada[dicio]
        return tratada

