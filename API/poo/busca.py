from operations import Operations
import json

class Busca(Operations):

    def __init__(self, mysql):
        super().__init__(mysql)

    def execute(self, request):
        self.abrirCursor()
        self.accessData(request)
        jPtList = []
        tables = self.separarEntradaGeral(self.data, jPtList) 
        result = self.buscaJuncao(tables, jPtList) 
        self.fecharCursor()
        return result

    def listarColunas(self):
        return [x[0] for x in self.cursor.description]

    def tupleToDict(self, tupla: tuple, colunas):
        dicio = {}
        for idx in range(len(tupla)):
            columnName = self.getOutputTableName(idx) + "." + colunas[idx]
            dicio[columnName] = tupla[idx]
        return dicio

    def getTablesLen(self):
        tDict = self.entradaFormatada
        tables = list(tDict.keys())
        tLen = {}
        for table in tables:
            tLen[table] = len(tDict[table])
        return tLen

    def getOutputTableName(self, idx):
        tIdx = -1
        tLen = self.getTablesLen()
        tables = list(tLen.keys())
        while idx >= 0 and tIdx < len(tables) - 1:
            tIdx += 1
            idx -= tLen[tables[tIdx]]
        return str(tables[tIdx])


    def outputFormatting(self, output):
        colunas = self.listarColunas()
        formatted = []
        for item in output:
            formatted.append(self.tupleToDict(item, colunas))
        return formatted

    def findColumnIntersecs(self, tables):
        intersecs = {}
        for table in tables:
            currentTab = tables[table]
            for column in currentTab.keys():
                if column not in intersecs:
                    intersecs[column] = [table]
                else:
                    intersecs[column].append(table)
        return intersecs

    def gerarQueryCompleta(self, tables, jPtList):
        query = """SELECT DISTINCT *
                    FROM """
        tList = [str(key) for key in tables.keys()]
        for idx in range(len(tList)):
            query += tList[idx]
            if idx < len(tList) - 1:
                query += ","
            query += " "
        searchFilters = self.gerarFiltros(tables)
        juncFilters = self.gerarFiltrosJunc(tables, jPtList)
        if searchFilters != "" or juncFilters != "":
            query += "WHERE "
        query += searchFilters
        if searchFilters == "":
            juncFilters = juncFilters[5:]
        query += juncFilters + ";"
        return query

    def gerarFiltrosJunc(self, tables, jPtList):
        intersecs = self.findColumnIntersecs(tables)
        fJunc = str("")
        for jp in jPtList:
            keyIntersec = intersecs[jp]
            for idx1 in range(len(keyIntersec)):
                for idx2 in range(idx1 + 1, len(keyIntersec)):
                    fJunc += f" AND {keyIntersec[idx1]}.{jp} = {keyIntersec[idx2]}.{jp}"
        return fJunc

    def gerarFiltros(self, tables):
        filtros = str("")
        for table in tables:
            currentTab = tables[table]
            for campo in currentTab:
                if currentTab[campo] != "NULL":
                    if filtros != "":
                        filtros += "AND "
                    filtros += table + "." + campo + " = " + currentTab[campo] + " "
        return filtros

    def buscaJuncao(self, tables, jPtList):
        busca = self.gerarQueryCompleta(tables, jPtList)
        self.cursor.execute(busca)
        result = self.cursor.fetchall()
        return self.outputFormatting(result)
        
    def separarEntradaGeral(self, entrada, jPtList):
        tratada = {}
        dictCounter = 0
        for dicio in entrada:
            match dicio:
                case "evento":
                    dicios = self.dividir_dicts(entrada[dicio], ["nome"])
                    dicios[1]["event_id"] = "NULL"
                    dicios[1]["details_id"] = "NULL"
                    tratada["Eventos"] = dicios[1]
                    dicios[0]["details_id"] = "NULL"
                    tratada["Det_eventos"] = dicios[0]
                    jPtList.append("event_id")
                    jPtList.append("details_id")
                    dictCounter += 1
                case "local":
                    dicios = self.dividir_dicts(entrada[dicio], ["nome"])
                    dicios[1]["local_id"] = "NULL"
                    dicios[1]["add_id"] = "NULL"
                    tratada["Locais"] = dicios[1]
                    dicios[0]["add_id"] = "NULL"
                    tratada["Enderecos"] = dicios[0]
                    jPtList.append("local_id")
                    jPtList.append("add_id")
                    dictCounter += 1
                case "pacote":
                    entrada["pacote"]["pack_id"] = "NULL"
                    tratada["Pacotes"] = entrada["pacote"]
                    jPtList.append("pack_id")
                    dictCounter += 1
                case _:
                    tratada[dicio] = entrada[dicio]
        if dictCounter > 1:
            tratada["Sediar"] = {
                "sed_id": "NULL",
                "event_id": "NULL",
                "local_id": "NULL",
                "pack_id": "NULL"
            }
        self.entradaFormatada = tratada
        return tratada


