from insercao import Insercao
from busca import Busca
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'sql10.freesqldatabase.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'sql10582776'
app.config['MYSQL_DATABASE_PASSWORD'] ='hhFr2ZKQML'
app.config['MYSQL_DATABASE_DB'] = 'sql10582776'
mysql.init_app(app)
        

@app.route('/busca', methods=['PATCH'])
@cross_origin()
def realizarBusca():
    busca = Busca(mysql)  # type: ignore
    result = busca.execute(request)
    return result

@app.route('/criar', methods=['POST'])  # type: ignore
@cross_origin()
def registrarDado():
    insercao = Insercao(mysql)  # type: ignore
    result = insercao.execute(request)
    return result


if __name__=='__main__':
    app.run(debug=True,port=5000)
