class Bucket:
    def __init__(self, fr):
        self.tuplas = []
        self.fr = fr

    def adicionar_tupla(self, tupla):
        if len(self.tuplas) < self.fr:
            self.tuplas.append(tupla)
            return True
        return False