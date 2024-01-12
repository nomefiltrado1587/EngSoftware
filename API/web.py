from flask import Flask,Response, request
from flaskext.mysql import MySQL
from pymysql import Error

app= Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'sql10.freemysqlhosting.net'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'sql10538868'
app.config['MYSQL_DATABASE_PASSWORD'] ='W24QHdFh3k'
app.config['MYSQL_DATABASE_DB'] = 'sql10538868'
mysql.init_app(app)



def format_data(data):
    for key in data:
        if data[key] !=0 and not data[key]:
            data[key] = 'NULL'
        elif type(data[key]) is str and not data[key].isnumeric():
            data[key] = "'"+data[key]+"'"



@app.route('/<table>', methods=['GET'])
def get_all(table):
    connection = mysql.connect()
    if(connection.open):
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()
        for row in result:
            print(row)
        cursor.close()
        connection.close()
        return "<p>Connection worked<p>"  
    return "<p>Connection failed<p>"

@app.route('/<table>', methods=['POST'])
def create_line(table):
    connection = mysql.connect()
    if(connection.open):
        exec("create_" + table + "()")  
        return "<p>Connection worked<p>"   
    return "<p>Connection failed<p>"

def create_evento():
    tipo = {'arte', 'música', 'geek', 'comédia', 'peça', 'festa'}
    connection = mysql.connect()
    cursor = connection.cursor()
    if(not connection.open):
        return "Connection failed"
    if(request.is_json):
        try:
            data = request.json
            if data['tipo'] not in tipo:
                raise Error("invalid tipo")
            format_data(data)
            if(not data['id']):
                cursor.execute(f'INSERT INTO Eventos(nome) VALUES({data["nome"]});')
                id_evento = cursor.lastrowid
            else:
                id_evento = data['id']
            cursor.execute(f'INSERT INTO Det_eventos (event_id, tipo, ev_status, descricao,avaliacao) VALUES({id_evento}, {data["tipo"]}, {data["ev_status"]},{data["descricao"]},{data["avaliacao"]});')
            connection.commit()
            cursor.close()
            connection.close()
            return "<p>Connection worked<p>"        
        except connection.Error as error:
            print(error)
            cursor.close()
            connection.close()
            return("error")
    else:
        cursor.close()
        connection.close()
        return Response("invalid post body, please send a json",status=400)



@app.route('/locais/<localId>',methods=['POST'])
def create_local(localID):

    connection = mysql.connect()
    cursor = connection.cursor()
    if(not connection.open):
        return "Connection failed"
    if(request.is_json):
        data = request.json
        print(type(data["nome"]))
        print(type(data["id"]))
        cursor.execute(f'INSERT INTO Locais(nome, add_id) VALUES(\'{data["nome"]}\', {data["id"]});')
        connection.commit()
        cursor.close()
        connection.close()
        return "<p>Connection worked<p>"        
    else:
        cursor.close()
        connection.close()
        return Response("invalid post body, please send a json",status=400)





def create_Pacotes():

    connection = mysql.connect()
    cursor = connection.cursor()
    if(not connection.open):
        return "Connection failed"
    if(request.is_json):
        try:
                data = request.json
                format_data(data)
                cursor.execute(f'INSERT INTO Pacotes (nome, dia, preco) VALUES({data["nome"]}, {data["dia"]}, {data["preco"]});')
                connection.commit()
                cursor.close()
                connection.close()
                return "<p>Connection worked<p>"
        except connection.Error as error:
            print(error)
            cursor.close()
            connection.close()
            return("error")
    else:
        cursor.close()
        connection.close()
        return Response("invalid post body, please send a json",status=400)


def create_sediar():
    
        connection = mysql.connect()
        cursor = connection.cursor()
        if(not connection.open):
            return "Connection failed"
        if(request.is_json):
            data = request.json
            try:
                print(type(data["event_id"]))
                print(type(data["pack_id"]))
                cursor.execute(f'INSERT INTO Sediar (event_id, pack_id, local_id) VALUES(\'{data["event_id"]}\', {data["pack_id"]}, {data["local_id"]});')
                connection.commit()
                cursor.close()
                connection.close()
                return "<p>Connection worked<p>"
            except connection.Error as error:
                    print(error)
                    cursor.close()
                    connection.close()
                    return("error")
        else:
            cursor.close()
            connection.close()
            return Response("invalid post body, please send a json",status=400)


def create_Enderecos():
        connection = mysql.connect()
        cursor = connection.cursor()
        if(not connection.open):
            return "Connection failed"
        if(request.is_json):
            data = request.json
            format_data(data)
            cursor.execute(f"INSERT INTO Enderecos (pais, estado, cidade, rua, numero, complemento) VALUES ({data['pais']},{data['estado']},{data['cidade']},{data['rua']}, {data['numero']}, {data['complemento']});")
            connection.commit()
            return "worked"
        else:
            return Response("invalid post body, please send a json",status=400)


def insert_into_Enderecos(data,cursor):
    if(data['complemento']=='NULL'):
        cursor.execute(f"SELECT add_id FROM Enderecos WHERE pais={data['pais']} AND estado={data['estado']} AND cidade={data['cidade']} AND rua={data['rua']} AND numero={data['numero']}")
        result = cursor.fetchall()
    else:
        cursor.execute(f"SELECT add_id FROM Enderecos WHERE pais={data['pais']} AND estado={data['estado']} AND cidade={data['cidade']} AND rua={data['rua']} AND numero={data['numero']} AND complemento={data['complemento']}")
        result = cursor.fetchall()

    
    if(len(result)==0):
        cursor.execute(f"INSERT INTO Enderecos (pais, estado, cidade, rua, numero, complemento) VALUES ({data['pais']},{data['estado']},{data['cidade']},{data['rua']}, {data['numero']}, {data['complemento']});")
        return cursor.lastrowid
        
    return result[0][0]



def create_Locais():
        connection = mysql.connect()
        cursor = connection.cursor()
        if(not connection.open):
            return "Connection failed"
        if(request.is_json):
            data = request.json
            format_data(data)

            add_id = insert_into_Enderecos(data,cursor)

            cursor.execute(f'INSERT INTO Locais(nome, add_id) VALUES({data["nome"]}, {add_id});')
            connection.commit()    
            return 'worked'            
        else:
            return Response("invalid post body, please send a json",status=400)

def filtros_query_evento(nome, tipo, status, min_aval, max_aval):

    where_nome_ev = """ AND ev.nome = """

    where_tipo = """ AND d.tipo = """

    where_status = """ AND d.status = """

    where_avaliac = """ AND d.avaliacao """

    where_ev = ""
    if (nome != 'NULL'):
        where_ev += where_nome_ev + nome
    if (tipo != 'NULL'):
        where_ev += where_tipo + "("
        for idx in range(len(tipo)):
            where_ev += tipo[idx]
            if (idx < len(tipo) - 1):
                where_ev += " OR "
        where_ev += ")"
    if (status != 'NULL'):
        where_ev += where_status + "("
        for idx in range(len(status)):
            where_ev += status[idx]
            if (idx < len(tipo) - 1):
                where_ev += " OR "
        where_ev += ")"
    if (min_aval != 'NULL'):
        where_ev += where_avaliac + "> " + min_aval
    if (max_aval != 'NULL'):
        where_ev += where_avaliac + "< " + max_aval
    return where_ev

def filtros_query_local(nome, rua, numero, complemento, cidade, estado, pais):

    where_nome_l = """ AND l.nome = """

    where_rua = """ AND en.rua = """

    where_numero = """ AND en.numero = """

    where_comp = """ AND en.complemento = """

    where_cidade = """ AND en.cidade = """

    where_estado = """ AND en.estado = """

    where_pais = """ AND en.pais = """

    where_loc = ""
    if (nome != 'NULL'):
        where_loc += where_nome_l + nome
    if (rua != 'NULL'):
        where_loc += where_rua + rua
    if (numero != 'NULL'):
        where_loc += where_numero + numero
    if (complemento != 'NULL'):
        where_loc += where_comp + complemento
    if (cidade != 'NULL'):
        where_loc += where_cidade + cidade
    if (estado != 'NULL'):
        where_loc += where_estado + estado
    if (pais != 'NULL'):
        where_loc += where_pais + pais
    return where_loc

def montar_query_busca(data):

    select_body = """SELECT ev.nome AS 'Nome do evento', 
            d.tipo AS 'Tipo do evento', 
            d.ev_status AS 'Status', 
            d.avaliacao AS 'Avaliação', 
            l.nome AS 'Nome do local', 
            CONCAT(en.rua, ', ', en.numero, ', ', en.complemento, '. ', en.cidade, ' - ', en.estado, ', ', en.pais, '.') AS 'Endereço' """
    from_body = """FROM Eventos AS ev, Det_eventos AS d, Locais AS l, Enderecos AS en """
    where_body_1 = """WHERE
                            ev.event_id = d.event_id AND
                            en.add_id = l.add_id AND
                            (ev.event_id, l.local_id) IN (
                                SELECT DISTINCT s.event_id, s.local_id
                                FROM Sediar AS s
                            )"""
    where_ev = filtros_query_evento(data["ev_nome"], data["tipo"], data["ev_status"], data["min_aval"], data["max_aval"])
    where_loc = filtros_query_local(data["l_nome"], data["rua"], data["numero"], data["complemento"], data["cidade"], data["estado"], data["pais"])
    query_compl = select_body + from_body + where_body_1 + where_ev + where_loc + ";"
    return query_compl

@app.route('/busca', methods=['GET'])
def busca_eventos():
    connection = mysql.connect()
    cursor = connection.cursor()
    if (not connection.open):
        return "Connection failed"
    if (request.is_json):
        data = request.json
        format_data(data)
        busca = montar_query_busca(data)
        cursor.execute(busca)
        result = cursor.fetchall()
        return render_template('res_busca.html', result=result)

    else:
        return Response("invalid post body, please send a json", status = 400)


@app.route('/locais',methods=['POST'])
def create_locais():
        connection = mysql.connect()
        cursor = connection.cursor()
        if(not connection.open):
            return "Connection failed"
        if(request.is_json):
            data = request.json
            format_data(data)
            if(data['complemento']=='NULL'):
                cursor.execute(f"SELECT add_id FROM Enderecos WHERE pais={data['pais']} AND estado={data['estado']} AND cidade={data['cidade']} AND rua={data['rua']} AND numero={data['numero']}")
                result = cursor.fetchall()
            else:
                cursor.execute(f"SELECT add_id FROM Enderecos WHERE pais={data['pais']} AND estado={data['estado']} AND cidade={data['cidade']} AND rua={data['rua']} AND numero={data['numero']} AND complemento={data['complemento']}")
                result = cursor.fetchall()
            print(type(result))
            print(len(result))
            if(len(result)==0):
                cursor.execute(f"INSERT INTO Enderecos (pais, estado, cidade, rua, numero, complemento) VALUES ({data['pais']},{data['estado']},{data['cidade']},{data['rua']}, {data['numero']}, {data['complemento']});")
                add_id = cursor.lastrowid
            else:
                add_id = result[0][0]

            cursor.execute(f'INSERT INTO Locais(nome, add_id) VALUES({data["nome"]}, {add_id});')
            connection.commit()
            cursor.close()  
            connection.close()  
            return 'worked'            
        else:
            cursor.close()
            connection.close()
            return Response("invalid post body, please send a json",status=400)
if __name__=='__main__':
    app.run(debug=True,port=5000)