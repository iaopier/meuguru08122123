from datetime import datetime, timedelta, date, time
from MVC.Model.voo import Voo
from MVC.Model.cadastro import Cadastro
from MVC.Model.cliente import Cliente
import csv


# classe de controle, realiza toda a logica de negocio entre visao e modelo
class Controle:
    def __init__(self):
        self.cadastro = Cadastro()
        self.__load_voo_csv()
        self.__load_cliente_csv()

    # realiza a listagem de voos com assentos livres com data e destino
    def lista_voos_destino_assentos(self, data, destino):
        # obtem lista de voos correntes carregadas
        voos = self.cadastro.get_voos()
        voos_data_destino = []
        # faz o tratamento de datas que o cliente informou
        data, tempo = self.__date_treatment(data)
        # cria um timestamp baseado na data que o cliente informou
        data_time_stamp = datetime(data.year, data.month, data.day, tempo.hour, tempo.minute, 0)
        # itera sobre a lista de voos comparando se o destino e data correspondem a algum
        # voo
        for voo in voos:
            # compara destino e data
            if voo.destino.replace(' ', '').upper() == destino.replace(' ', '').upper() and \
                    voo.data == data_time_stamp:
                # se existir voo, adiciona na lista
                voos_data_destino.append(voo)
                # retorna a lista de voos
        return voos_data_destino

    def lista_voos_paradas_datas(self, busca):
        # obtem lista de voos correntes carregadas
        voos = self.cadastro.get_voos()
        voos_data_paradas = []
        # faz o tratamento de datas que o cliente informou
        data = self.__date_treatment(busca)
        # se o cliente informou uma data que foi de fato tratada ele buscara por datas
        if data:
            # cria uma data de inicio, que e a data que o cliente pediu
            data_ini, tempo = self.__date_treatment(busca)
            # cria um timestamp dessa dada para comparacao
            data_ini_time_stamp = datetime(data_ini.year, data_ini.month, data_ini.day, tempo.hour, tempo.minute, 0)
            # cria uma data final, sempre ao final do dia
            data_final, tempo = self.__date_treatment(busca + " 23:59")
            # cria um timestamp
            data_final_time_stamp = datetime(data_final.year,
                                             data_final.month,
                                             data_final.day,
                                             tempo.hour,
                                             tempo.minute,
                                             0)
            # itera sobre a lista de voos
            for voo in voos:
                # se o voo tem data entre a inicial e final ele adiciona
                # na lista de voos
                if data_ini_time_stamp <= voo.data <= data_final_time_stamp:
                    voos_data_paradas.append(voo)
        # caso o usuario informou uma parada
        elif not data:
            # itera sobre a lista de voos
            for voo in voos:
                # busca se a parada existe em algum dos voos e se existir, insere na lista
                if busca.replace(' ', '').upper() in voo.paradas:
                    voos_data_paradas.append(voo)
        # retorna a lista de voos
        return voos_data_paradas

    # cadastro de voos
    def cadastro_voos(self, data, periodicidade, assentos, lista_cidades):
        # cria uma data e hora informados pelo usuario
        data, tempo = self.__date_treatment(data)
        lista_cidades = lista_cidades.upper()
        # separa a string de cidades em um lista de cidades
        cidades = lista_cidades.split(',')
        # obtem uma sublista com origem e destino
        origem_destino = cidades[::len(cidades) - 1]
        # remove da lista de cidades origem e destino
        cidades.remove(origem_destino[0])
        cidades.remove(origem_destino[1])
        # marca o tamanho da lista de voos para criar ids de voos
        size_list = len(self.cadastro.get_voos())
        # cria uma data maxima, e possivel cadastra somente voos por meses
        # se uma data for diaria, cadastrara 1 voo por dia restante do mes
        # se for uma data semanal, cadastrara 1 voo por semana restante
        # da data informada
        data_final = self.__last_day_of_month(data)
        # verifica a periodicidade do voo
        if periodicidade == '1':
            # quando o voo e diario, e a data estiver dentro do limite maximo do mss
            while datetime(int(data.year), int(data.month), int(data.day), int(tempo.hour), int(tempo.minute)) < \
                    datetime(data_final.year, data_final.month, data_final.day, 0, 0):
                # cria um timestamp com a data que o cliente informou
                data_time_stamp = datetime(int(data.year),
                                           int(data.month),
                                           int(data.day),
                                           int(tempo.hour),
                                           int(tempo.minute))
                # cria novo objeto voo, com os dados informados
                voo = Voo(origem_destino[0], origem_destino[1],
                          data_time_stamp, periodicidade,
                          assentos, cidades, size_list)
                # adiciona na lista geral de voos
                self.cadastro.set_voos(voo)
                # itera sobre o numero de voos, para manter o id correto
                size_list = len(self.cadastro.get_voos())
                # modifica a data original por 1 dia para criar o proximo voo diario
                data = data + timedelta(days=1)
        # caso o voo seja semanal, e a data estiver dentro do limite maximo do mes
        elif periodicidade == '2':
            while datetime(int(data.year), int(data.month), int(data.day), int(tempo.hour), int(tempo.minute)) < \
                    datetime(data_final.year, data_final.month, data_final.day, 0, 0):
                # cria um timestamp com a data que o cliente informou
                data_time_stamp = datetime(int(data.year),
                                           int(data.month),
                                           int(data.day),
                                           int(tempo.hour),
                                           int(tempo.minute))
                # cria novo objeto voo, com os dados informados
                voo = Voo(origem_destino[0], origem_destino[1], data_time_stamp, periodicidade, assentos, cidades,
                          size_list)
                # adiciona na lista geral de voos
                self.cadastro.set_voos(voo)
                # itera sobre o numero de voos, para manter o id correto
                size_list = len(self.cadastro.get_voos())
                # modifica a data original por 7 dias para criar o proximo voo semanal
                data = data + timedelta(days=7)
        # escreve os voos no arquivo de armazenamento
        self.__persist_voo_csv()

    # venda de bilhete
    def venda_bilhete(self, data, origem, destino, documento, nome, sobrenome):
        # obtem os voos do sistema
        voos = self.cadastro.get_voos()
        # obtem a data que o cliente informou
        data, tempo = self.__date_treatment(data)
        # cria um timestamp com os valores que o cliente informou para o voo
        data_hora_voo = datetime(data.year,
                                 data.month,
                                 data.day,
                                 tempo.hour,
                                 tempo.minute,
                                 0)
        # itera sobre os voos
        for voo in voos:
            # checa se existe um voo com a data e cidade de origem
            # se nao existirem nao precisa checar mais nada
            if voo.data == data_hora_voo and voo.origem.replace(' ', '').upper() == origem.replace(' ', '').upper():
                # caso existam, realizara a busca por destino, ou por parada e assentos vazios
                if voo.destino.replace(' ', '').upper() == destino.replace(' ', '').upper() or (
                        (destino.upper() in voo.paradas)) and \
                        voo.assentos > 0:
                    # decrementa caso seja possivel comprar o voo, o numero de assentos
                    voo.assentos = voo.assentos - 1
                    # modifica o voo para atualizar os assentos no csv
                    voos[int(voo.id)] = voo
                    # cria um cliente
                    cliente = Cliente(documento, nome, sobrenome)
                    self.__cadastro_cliente(cliente)
                    # persiste o voo no csv com dados atualizados
                    self.__persist_voo_csv()
                    # persiste as informacoes do cliente que comprou o voo
                    # com o id do voo em que ele estara
                    self.__persist_cliente_csv(voo.id)
                    return True
        return False

    # perssistencia de voo no csv
    # metodo privado pois so e acessado pela classe
    def __persist_voo_csv(self):
        # colunas que ficam no header do arquivo csv
        colunas = ["origem", "destino", "data", "periodicidade", "assentos", "paradas", "id"]
        # obtem a lista de voos do sistema
        voos = self.cadastro.get_voos()
        # abre o arquivo de voo com permissao de escrita
        with open('voos_file', 'w') as f:
            # abre o arquivo no write
            write = csv.writer(f)
            # escreve o header
            write.writerow(colunas)
            # itera sobre os voos
            for voo in voos:
                # cria as roows para cada voo
                voo_row = [voo.origem, voo.destino, voo.data, voo.periodicidade, voo.assentos, voo.paradas, voo.id]
                # escreve no arquivo os voos
                write.writerow(voo_row)
        # chama a carga de voos do csv, para manter a memoria sempre atualizada, sem
        # necessitar finalizar o programa
        self.__load_voo_csv()

    # classe privada de carga de voos do csv
    def __load_voo_csv(self):
        voos = []
        # abre o arquivo com leitura para os voos
        with open('voos_file', 'r') as f:
            # faz a leitura
            read = csv.reader(f)
            # pula a linha de header
            next(read, None)
            # itera sobre a linhas
            for row in read:
                # remove carateres indesejados das colunas que guardam
                # a lista de paradas
                # separa essa string em uma lista
                paradas = row[5]
                # cria objetos em memoria para todos os voos encontrados
                # usa formatacao de datetime
                voo = Voo(row[0], row[1], datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"), row[3],
                          int(row[4]), paradas, row[6])
                # adiciona os voos na lista corrente em memoria
                voos.append(voo)
        # chama o setter de voos com essa lista
        self.cadastro.load_voos(voos)

    # classe privada de persistencia de cliente
    def __persist_cliente_csv(self, id_do_voo):
        # header do arquivo
        colunas = ["documento", "nome", "sobrenome", "id_do_voo"]
        # obtem a lista corrente de clientes em memoria
        clientes = self.cadastro.get_clientes()
        # abre o arquivo de clientes
        with open('clientes_file', 'w') as f:
            write = csv.writer(f)
            write.writerow(colunas)
            # itera sobre os clientes
            for cliente in clientes:
                # cria rows para os clientes serem inseridos no csv
                # caso o cliente nao tenha voo, adiciona o id do voo
                if cliente.id_voo == -1:
                    cliente_row = [cliente.documento, cliente.nome, cliente.sobrenome, id_do_voo]
                else:
                    cliente_row = [cliente.documento, cliente.nome, cliente.sobrenome, cliente.id_voo]
                # ao final um cliente sempre tem um id de voo para um voo especifico que ele comprou
                # escreve no arquivo csv
                write.writerow(cliente_row)
        # chama o setter de clientes com essa lista
        self.__load_cliente_csv()

    # classe privada que carrega os clientes do arquivo para memoria
    def __load_cliente_csv(self):
        clientes = []
        # abre arquivo de cliente com leitura
        with open('clientes_file', 'r') as f:
            read = csv.reader(f)
            # pula o header
            next(read, None)
            # itera sobre as linhas do arquivo
            for row in read:
                # cria clientes com os dados
                cliente = Cliente(row[0], row[1], row[2])
                cliente.id_voo = row[3]
                # adiciona na lista de clientes corrente um novo cliente
                clientes.append(cliente)
        # chama o setter de clientes
        self.cadastro.load_clientes(clientes)

    # metodos estaticos de transformacoes
    @staticmethod
    # tratamento de data
    def __date_treatment(data):
        # se o usuario de fato passou uma data
        if '-' in data:
            # separa a string em uma lista
            data_dmy = data.split("-")
            # separa a parte de horas da data
            data_dmy_hms = str(data_dmy[2]).split(" ")
            # caso exista hora e minuto na data
            # criara uma string de hora e data com os valores que o cliente informou
            if len(data_dmy_hms) > 1 and data_dmy_hms[1] != "":
                time_hm = data_dmy_hms[1].split(":")
                time_hm = time(int(time_hm[0]), int(time_hm[1]))
            # caso contrario, preenche com hora e minuto padrao
            else:
                time_hm = time(0, 0)
            # retorna uma data e um tempo
            return date(int(data_dmy_hms[0]), int(data_dmy[1]), int(data_dmy[0])), time_hm
        # caso o usuario nao passou uma data, retorna falso
        else:
            return False

    # calcula o ultimo dia do mes a partir da data inserida
    # para controlar a criacao de voos para no maximo dentro do mes
    @staticmethod
    def __last_day_of_month(data):
        if data.month == 12:
            return data.replace(day=31)
        return data.replace(month=data.month + 1, day=1)

    # cadastra clientes
    def __cadastro_cliente(self, cliente):
        self.cadastro.set_clientes(cliente)
