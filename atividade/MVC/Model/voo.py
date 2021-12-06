# classe de voo, armazena informacoes dos voos criados pelo usuario
class Voo:
    assentos = 0
    paradas = []

    # construtor
    def __init__(self, origem, destino, data, periodicidade, assentos, paradas, id):
        self.origem = origem
        self.destino = destino
        self.data = data
        self.periodicidade = periodicidade
        self.assentos = assentos
        self.paradas = paradas
        self.id = id
