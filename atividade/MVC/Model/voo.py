import uuid

class Voo:
    assentos = 0
    def __init__(self, origem, destino, data, periodicidade, assentos, paradas,id):
        self.origem = origem
        self.destino = destino
        self.data = data
        self.periodicidade = periodicidade
        self.assentos = assentos
        self.paradas = paradas
        self.id = id
