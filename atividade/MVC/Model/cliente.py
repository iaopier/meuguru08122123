# classe de cliente
# o cliente comeca com id de voo -1 e depois esse valor e trocado pelo
# voo em que o cliente estara
class Cliente:
    id_voo = -1

    def __init__(self, documento, nome, sobrenome):
        self.documento = documento
        self.nome = nome
        self.sobrenome = sobrenome
