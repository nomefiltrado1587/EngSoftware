from test_createEvent import TestCreateEvent
from test_createLocal import TestCreateLocal
from test_createPacote import TestCreatePacote

def SelectTest(test):
    if(test=="evento"):
        return TestCreateEvent()
    elif(test=="local"):
        return TestCreateLocal()
    elif(test=="pacote"):
        return TestCreatePacote()
    else:
        return -1


def main():
    url="http://127.0.0.1:5500/public/mainPage/"
    test_type = input("insert the unit you want to test (evento, local or pacote)\n")
    create_event = SelectTest(test_type)
    if(create_event==-1):
        print("please select a valid unit (evento, local or pacote)")
        return 0
    file_name = input()
    arqv = open(file_name)
    lineNum=0
    for line in arqv:
        params_list = line.strip().split(",")
        if(test_type=="evento"):
            create_event.setup_method(endereco_inicial=url,  # type: ignore
            nome=params_list[0],
            tipo=params_list[1],
            avaliacao=params_list[2],
            descricao=params_list[3])
        if(test_type=="local"):
            create_event.setup_method(endereco_arq=url, # type: ignore
            nome=params_list[0],
            pais=params_list[1],
            estado=params_list[2],
            cidade=params_list[3],
            nome_rua=params_list[4],
            numero=params_list[5],
            complemento=params_list[6])
        elif(test_type=="pacote"):
            create_event.setup_method(endereco=url, # type: ignore
            nome=params_list[0],
            dia= params_list[1],
            preco=params_list[2]
            )
        result = create_event.execute_test()
        if(params_list[-1]=='T'):
            if(result):
                print(f"test {lineNum} passed")
            else:
                print(f"test {lineNum} failed")
        else:
            if(not result):
                print(f"test {lineNum} passed")
            else:
                print(f"test {lineNum} failed")
        lineNum+=1
    arqv.close()
    return 0

if __name__ =="__main__":
    main()