from .tupla import Tupla
from .pagina import Pagina

class Tabela:
    def __init__(self):
        self.tuplas = []
        self.paginas = []

    def adicionar_tupla(self, tupla, tamanho_pagina):
        if not self.paginas or len(self.paginas[-1].tuplas) >= tamanho_pagina:
            self.paginas.append(Pagina(tamanho_pagina))
        self.paginas[-1].adicionar_tupla(tupla)
        self.tuplas.append(tupla)