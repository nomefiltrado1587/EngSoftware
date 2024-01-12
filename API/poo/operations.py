from flask import Flask, request
from flaskext.mysql import MySQL
from pymysql import Error
import json

class Operations:

    def __init__(self, mysql):
        self.mysql = mysql

    def abrirCursor(self):
        self.connection = self.mysql.connect()
        if(self.connection.open):
            self.cursor = self.connection.cursor()
            return "<p>Connection worked<p>"
        else:
            return "<p>Connection failed<p>"

    def format_data(self, data):
        formatado = data.copy()
        for key in data:
            if data[key] !=0 and not data[key]:
                formatado[key] = 'NULL'
            elif type(data[key]) is str and not data[key].isnumeric():
                formatado[key] = "'"+data[key]+"'"
        return formatado

    def dividir_dicts(self, dicio, fieldList):
        novo = dict()
        dicios = [dicio, novo]
        for field in fieldList:
            novo[field] = dicio[field]
            dicio.pop(field)
        return dicios

    def accessData(self, request):
        if(request.is_json):
            tables = request.json
            data = {}
            for table in tables:
                data[table] = self.format_data(tables[table])
            self.data = data

    def execute(self, request):
        pass

    def fecharCursor(self):
        self.cursor.close()
        self.connection.close()
