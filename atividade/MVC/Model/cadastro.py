class Cadastro:
    def __init__(self):
        self.voos = []

    # getter method
    def get_voos(self):
        return self.voos

    # setter method
    def set_voos(self, voo):
        self.voos.append(voo)


