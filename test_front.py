from testes.frontEndTests.test_createEvent import TestCreateEvent
from testes.frontEndTests.test_createLocal import TestCreateLocal
from testes.frontEndTests.test_createSediar import TestCreateSediar
from testes.frontEndTests.test_createPacote import TestCreatePacote
import sys
ENDERECO_PAGINA_INICIAL = "/public/mainPage/index.html"
PATH_TESTS = "testes/frontEndTests/arqvs/"

def extrairDadosDeTeste(nome):
    nomeArq = PATH_TESTS+nome
    arqEntrada = open(nomeArq+".in","r")
    entrada = arqEntrada.readline()
    arqSaida = open(nomeArq+".res","r")
    saida = arqSaida.readline()

    return entrada.split(","),saida



def main():
    args = sys.argv
    testClasses = [TestCreateEvent,TestCreateLocal,TestCreateSediar,TestCreatePacote]

    test = testClasses[int(args[1])]()


    entrada,saidaEsperada = extrairDadosDeTeste(args[2])

    test.setup_method(ENDERECO_PAGINA_INICIAL,*entrada)

    try:
        test.execute_test()
    except:
        print("Deu ruinzao")

    



    pass

if __name__ == "__main__":
    main()