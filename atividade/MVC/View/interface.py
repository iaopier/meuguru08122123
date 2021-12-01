from MVC.Controller.controle import Controle


def lista_voos_destino_assentos_data(self):
    print("Lista de Voos por destino e data")
    print("Informe a data (dd-MM-yyyy)")
    data = input()
    print("Informe o destino")
    destino = input()
    voos_data_destino = self.controle.lista_voos_destino_assentos(data, destino)
    for voo in voos_data_destino:
        print("Informacoes do voo " + str(voo.data)
              + " Destino " + str(voo.destino)
              + " Assentos Disponíveis " + str(voo.assentos))


def lista_voos_paradas_datas(self):
    print("Lista de Voos por parada")
    print("Informe a data (dd-MM-yyyy)")
    data = input()
    print("Informe a parada")
    parada = input()
    voos_data_parada = self.controle.lista_voos_paradas_datas(data, parada)
    for voo in voos_data_parada:
        print("Informacoes do voo " + str(voo.data)
              + " Parada " + str(parada)
              + " Assentos Disponíveis " + str(voo.assentos))


def cadastro_voos(self):
    print("Cadastro de Voo")
    print("Informe a data (dd-MM-yyyy)")
    data = input()
    print("Informe periodicidade")
    periodicidade = input()
    print("Informe a lista de cidades (origem,[paradas],destino")
    lista_cidades = input()
    print("Informe quantidade de assentos")
    assentos = input()
    self.controle.cadastro_voos(data, periodicidade, int(assentos), lista_cidades)


def venda_bilhete(self):
    print("Venda de bilhete")
    print("Informe a data (dd-MM-yyyy")
    data = input()
    print("Informe Origem do Voo")
    origem = input()
    print("Informe Destino do Voo")
    destino = input()
    if self.controle.venda_bilhete(data, origem, destino):
        print("Venda Realizada")
    else:
        print("Venda nao realizada")


class Interface:
    voos = []

    def __init__(self):
        self.voos = []
        self.controle = Controle()
        print("Opcoes disponiveis: \n"
              "Cadastrar Voo(1) \n"
              "Visualizar Voos com assentos disponíveis com data e destino(2) \n"
              "Visualizar Voos com paradas especificas e com data(3) \n"
              "Realizar venda de Bilhete(4) \n"
              "Sair(5)")
        opcao = input()
        while 5 > int(opcao) > 0:
            if int(opcao) == 1:
                cadastro_voos(self)
            elif int(opcao) == 2:
                lista_voos_destino_assentos_data(self)
            elif int(opcao) == 3:
                lista_voos_paradas_datas(self)
            elif int(opcao) == 4:
                venda_bilhete(self)

            print("Opcoes disponiveis: \n"
                    "Cadastrar Voo(1) \n"
                    "Visualizar Voos com assentos disponíveis com data e destino(2) \n"
                    "Visualizar Voos com paradas especificas e com data(3) \n"
                    "Realizar venda de Bilhete(4) \n"
                    "Sair(5)")
            opcao = input()
