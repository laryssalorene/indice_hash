class Pagina:
    def __init__(self, tamanho):
        self.tuplas = []
        self.tamanho = tamanho

    def adicionar_tupla(self, tupla):
        if len(self.tuplas) < self.tamanho:
            self.tuplas.append(tupla)
            return True
        return False