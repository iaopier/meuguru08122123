from datetime import datetime, timedelta, date
from MVC.Model.voo import Voo
from MVC.Model.cadastro import Cadastro
from MVC.Model.cliente import Cliente
import csv


class Controle:
    def __init__(self):
        self.cadastro = Cadastro()
        self.__load_voo_csv()
        self.__load_cliente_csv()

    def lista_voos_destino_assentos(self, data, destino):
        voos = self.cadastro.get_voos()
        voos_data_destino = []
        data_ini = self.__date_treatment(data)
        data_final = self.__date_treatment(data + " 23:59")
        for voo in voos:
            if voo.destino == destino and data_ini <= voo.data <= data_final:
                voos_data_destino.append(voo)
        return voos_data_destino

    def lista_voos_paradas_datas(self, busca):
        voos = self.cadastro.get_voos()
        voos_data_paradas = []
        data = self.__date_treatment(busca)
        if data:
            data_ini = self.__date_treatment(busca)
            data_final = self.__date_treatment(busca + " 23:59")
            for voo in voos:
                if data_ini <= voo.data <= data_final:
                    voos_data_paradas.append(voo)
        elif not data:
            for voo in voos:
                if busca in voo.paradas:
                    voos_data_paradas.append(voo)
        return voos_data_paradas

    def cadastro_voos(self, data, periodicidade, assentos, lista_cidades):
        data = self.__date_treatment(data)
        cidades = lista_cidades.split(',')
        origem_destino = cidades[::len(cidades) - 1]
        cidades.remove(origem_destino[0])
        cidades.remove(origem_destino[1])
        size_list = len(self.cadastro.get_voos())
        data_final = self.__last_day_of_month(data)
        if periodicidade == '1':
            while data < datetime(data_final.year, data_final.month, data_final.day, 0, 0, 0):
                voo = Voo(origem_destino[0], origem_destino[1], data, periodicidade, assentos, cidades, size_list)
                self.cadastro.set_voos(voo)
                size_list = len(self.cadastro.get_voos())
                data = data + timedelta(days=1)
        elif periodicidade == '2':
            while data < data_final:
                voo = Voo(origem_destino[0], origem_destino[1], data, periodicidade, assentos, cidades, size_list)
                self.cadastro.set_voos(voo)
                size_list = len(self.cadastro.get_voos())
                data = data + timedelta(days=7)
        self.__persist_voo_csv()

    def venda_bilhete(self, data, origem, destino, documento, nome, sobrenome):
        cliente = Cliente(documento, nome, sobrenome)
        self.__cadastro_cliente(cliente)
        voos = self.cadastro.get_voos()
        data = self.__date_treatment(data)
        for voo in voos:
            if origem == voo.origem and \
                    (voo.destino == destino or
                     destino in voo.paradas) and \
                    self.__date_treatment(voo.data) == data and \
                    voo.assentos > 0:
                voo.assentos = voo.assentos - 1
                voos[int(voo.id)] = voo
                self.__persist_voo_csv()
                self.__persist_cliente_csv(voo.id)
                return True
        return False

    def __persist_voo_csv(self):
        colunas = ["origem", "destino", "data", "periodicidade", "assentos", "paradas", "id"]
        voos = self.cadastro.get_voos()
        with open('voos_file', 'w') as f:
            write = csv.writer(f)
            write.writerow(colunas)
            for voo in voos:
                voo_row = [voo.origem, voo.destino, voo.data, voo.periodicidade, voo.assentos, voo.paradas, voo.id]
                write.writerow(voo_row)
        self.__load_voo_csv()

    def __load_voo_csv(self):
        voos = []
        with open('voos_file', 'r') as f:
            read = csv.reader(f)
            next(read, None)
            for row in read:
                voo = Voo(row[0], row[1], datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"), row[3],
                          int(row[4]), row[5], row[6])
                voos.append(voo)
        self.cadastro.load_voos(voos)

    def __persist_cliente_csv(self, id_do_voo):
        colunas = ["documento", "nome", "sobrenome", "id_do_voo"]
        clientes = self.cadastro.get_clientes()
        with open('clientes_file', 'w') as f:
            write = csv.writer(f)
            write.writerow(colunas)
            for cliente in clientes:
                cliente_row = [cliente.documento, cliente.nome, cliente.sobrenome, id_do_voo]
                write.writerow(cliente_row)
        self.__load_cliente_csv()

    def __load_cliente_csv(self):
        clientes = []
        with open('clientes_file', 'r') as f:
            read = csv.reader(f)
            next(read, None)
            for row in read:
                cliente = Cliente(row[0], row[1], row[2])
                cliente.id_voo = row[3]
                clientes.append(cliente)
        self.cadastro.load_clientes(clientes)

    @staticmethod
    def __date_treatment(data):
        try:
            data = data.split("-")
            data = data[1] + "-" + data[0] + "-" + data[2]
        except:
            return False
        try:
            return datetime.strptime(data, "%m-%d-%Y %H:%M")
        except ValueError:
            return datetime.strptime(data + " 00:00", "%m-%d-%Y %H:%M")

    @staticmethod
    def __last_day_of_month(data):
        if data.month == 12:
            return data.replace(day=31)
        return data.replace(month=data.month + 1, day=1)

    def __cadastro_cliente(self, cliente):
        self.cadastro.set_clientes(cliente)
