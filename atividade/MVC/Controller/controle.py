from MVC.Model.voo import Voo
from MVC.Model.cadastro import Cadastro
import csv


class Controle:
    def __init__(self):
        self.cadastro = Cadastro()

    def lista_voos_destino_assentos(self, data, destino):
        voos = self.cadastro.get_voos()
        voos_data_destino = []
        for voo in voos:
            if voo.destino == destino and voo.data == data:
                voos_data_destino.append(voo)
        return voos_data_destino

    def lista_voos_paradas_datas(self, data, parada):
        voos = self.cadastro.get_voos()
        voos_data_paradas = []
        for voo in voos:
            if parada in voo.paradas and voo.data == data:
                voos_data_paradas.append(voo)
        return voos_data_paradas

    def cadastro_voos(self, data, periodicidade, assentos, lista_cidades):
        cidades = lista_cidades.split(',')
        origem_destino = cidades[::len(cidades) - 1]
        cidades.remove(origem_destino[0])
        cidades.remove(origem_destino[1])
        voo = Voo(origem_destino[0], origem_destino[1], data, periodicidade, assentos, cidades)
        self.cadastro.set_voos(voo)
        self.persist_csv()

    def venda_bilhete(self, data, origem, destino):
        voos = self.cadastro.get_voos()
        for voo in voos:
            if origem == voo.origem and voo.destino == destino and voo.data == data and voo.assentos > 0:
                voo.assentos = voo.assentos - 1
                return True
        return False

    def persist_csv(self):
        colunas = ["origem", "destino", "data", "periodicidade", "assentos", "paradas"]
        voos = self.cadastro.get_voos()
        with open('GFG', 'w') as f:
            write = csv.writer(f)
            write.writerow(colunas)
            for voo in voos:
                voo_row = [voo.origem, voo.destino, voo.data, voo.periodicidade, voo.assentos, voo.paradas]
                write.writerow(voo_row)
        return 0
