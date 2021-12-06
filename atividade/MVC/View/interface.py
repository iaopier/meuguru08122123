from MVC.Controller.controle import Controle


def lista_voos_destino_assentos_data(self):
    # metodo da chamadas com destino e data
    while True:
        # recebe os dados necessarios
        print("Lista de Voos por destino e data")
        print("Informe a data (dd-MM-yyyy)")
        data = input()
        print("Informe o destino")
        destino = input()
        print("Deseja submeter os dados? s/n = (retornar ao menu anterior)/c = (corrigir)")
        # le se o usuario deseja prosseguir, corrigir dados ou cancelar
        op = input()
        if op == 's':
            # chama operacao de listagem com data e destino utilizados
            voos_data_destino = self.controle.lista_voos_destino_assentos(data, destino)
            # itera sobre os voos retornados
            for voo in voos_data_destino:
                print("Informacoes do voo " + str(voo.data)
                      + " Origem " + str(voo.origem)
                      + " Paradas " + str(voo.paradas)
                      + " Destino " + str(voo.destino)
                      + " Assentos Disponíveis " + str(voo.assentos))
            return
        elif op == 'c':
            # retorna ao inicio para ler de novo os dados
            pass
        elif op == 'n':
            # cancela a operacao
            return
        else:
            # espera uma opcao correta
            print("Operacao invalida!")


# lista os voos, ou por parada ou por data
def lista_voos_paradas_datas(self):
    while True:
        print("Lista de Voos por parada ou data")
        print("Informe a data e hora (dd-MM-yyyy) ou uma Parada")
        busca = input()
        print("Deseja submeter os dados? s/n = (retornar ao menu anterior)/c = (corrigir)")
        op = input()
        if op == 's':
            # chama operacao de listagem com data ou destino
            voos_data_parada = self.controle.lista_voos_paradas_datas(busca)
            # itera sobre os voos e informa quais foram encontrados
            for voo in voos_data_parada:
                print("Informacoes do voo " + str(voo.data)
                      + " Origem " + str(voo.origem)
                      + " Parada " + str(voo.paradas)
                      + " Destino " + str(voo.destino)
                      + " Assentos Disponíveis " + str(voo.assentos))
            return
        elif op == 'c':
            # retorna ao inicio para ler de novo os dados
            pass
        elif op == 'n':
            # cancela a operacao
            return
        else:
            # espera uma opcao correta
            print("Operacao invalida!")


def cadastro_voos(self):
    # metodo para chamar o cadastro de voos
    while True:
        print("Cadastro de Voo")
        print("Informe a data (dd-MM-yyyy HH:MM)")
        data = input()
        print("Informe periodicidade (1 - diario/ 2 - semanal")
        periodicidade = input()
        print("Informe a lista de cidades (origem,[paradas],destino")
        lista_cidades = input()
        print("Informe quantidade de assentos")
        assentos = input()
        print("Deseja submeter os dados? s/n = (retornar ao menu anterior)/c = (corrigir)")
        op = input()
        if op == 's':
            # realiza o cadastro de voos com os dados informados
            self.controle.cadastro_voos(data, periodicidade, int(assentos), lista_cidades)
            return
        elif op == 'c':
            # retorna ao inicio para ler de novo os dados
            pass
        elif op == 'n':
            # cancela a operacao
            return
        else:
            print("Operacao invalida!")


def venda_bilhete(self):
    # metodo que chama a venda de bilhetes
    while True:
        print("Venda de bilhete")
        print("Documento do Cliente")
        documento = input()
        print("Nome do Cliente")
        nome = input()
        print("Sobrenome do Cliente")
        sobrenome = input()
        print("Informe a data (dd-MM-yyyy HH:MM - Caso HH:MM = 00:00,comprará o voo do horário 00:00 caso haja)")
        data = input()
        print("Informe Origem do Voo")
        origem = input()
        print("Informe Destino do Voo")
        destino = input()
        print("Deseja submeter os dados? s/n = (retornar ao menu anterior)/c = (corrigir)")
        op = input()
        if op == 's':
            # se conseguir vender um bilhete com os dados informados, escreve em tela que ocorreu a venda
            if self.controle.venda_bilhete(data, origem, destino, documento, nome, sobrenome):
                print("Venda Realizada")
                return
            else:
                # se nao conseguir vender um bilhete com os dados informados, escreve em tela que nao ocorreu a venda
                print("Venda nao realizada, cheque os dados informados!")
                return
        elif op == 'c':
            # retorna ao inicio para ler de novo os dados
            pass
        elif op == 'n':
            # cancela a operacao
            return
        else:
            # espera uma opcao correta
            print("Operacao invalida!")


# classe de interface
class Interface:
    voos = []

    def __init__(self):
        # inicializa os voos
        # cria um objeto da classe de controle para
        # chamar seus metodos
        self.voos = []
        self.controle = Controle()
        print("Opcoes disponiveis: \n"
              "Cadastrar Voo(1) \n"
              "Visualizar Voos com assentos disponíveis com data e destino(2) \n"
              "Visualizar Voos com paradas especificas ou data(3) \n"
              "Realizar venda de Bilhete(4) \n"
              "Sair(5)")
        # leitor de escolha
        opcao = input()
        # controle de continuacao ou finalizado do programa
        # e opcoes a serem chamadas
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
                  "Visualizar Voos com paradas especificas ou data(3) \n"
                  "Realizar venda de Bilhete(4) \n"
                  "Sair(5)")
            opcao = input()
