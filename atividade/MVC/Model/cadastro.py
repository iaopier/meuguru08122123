# classe de cadastro, ela contem a lista de voos e clientes
# foram utilizados getters e setters explicitos pois, existem diferenças dos comuns, por
# setarem listas
class Cadastro:
    def __init__(self):
        self.voos = []
        self.clientes = []

    # getter method
    def get_voos(self):
        return self.voos

    # setter method
    def set_voos(self, voo):
        self.voos.append(voo)

    def load_voos(self, voos):
        self.voos = voos

    def get_clientes(self):
        return self.clientes

    def set_clientes(self, cliente):
        self.clientes.append(cliente)

    def load_clientes(self,clientes):
        self.clientes = clientes
