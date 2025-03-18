from .bucket import Bucket

class HashIndex:
    def __init__(self, nb, fr):
        """
        Inicializa o índice hash.
        
        :param nb: Número de buckets.
        :param fr: Número máximo de tuplas por bucket.
        """
        self.buckets = [Bucket(fr) for _ in range(nb)]  # Lista de buckets
        self.colisoes = 0  # Contador de colisões
        self.overflows = 0  # Contador de overflows

    def hash_function(self, chave):
        """
        Função hash que mapeia uma chave para um índice de bucket.
        
        :param chave: Chave de busca.
        :return: Índice do bucket.
        """
        return hash(chave) % len(self.buckets)

    def adicionar_tupla(self, tupla, pagina):
        """
        Adiciona uma tupla ao índice hash.
        
        :param tupla: Tupla a ser adicionada.
        :param pagina: Página onde a tupla está armazenada.
        :return: True se a tupla foi adicionada, False caso contrário.
        """
        index = self.hash_function(tupla.chave)
        if not self.buckets[index].adicionar_tupla((tupla, pagina)):
            self.colisoes += 1  # Incrementa colisões
            self.overflows += 1  # Incrementa overflows
            # Implementar resolução de colisões (ex: encadeamento)
            return False
        return True

    def buscar_tupla(self, chave):
        """
        Busca uma tupla no índice hash.
        
        :param chave: Chave de busca.
        :return: Tupla, página e custo (número de acessos).
        """
        index = self.hash_function(chave)
        custo = 1  # Custo inicial (acesso ao bucket)
        for tupla, pagina in self.buckets[index].tuplas:
            if tupla.chave == chave:
                return tupla, pagina, custo
            custo += 1  # Incrementa o custo para cada tupla verificada no bucket
        return None, None, custo  # Retorna None se a chave não for encontrada

    def get_estatisticas(self):
        """
        Retorna estatísticas do índice hash.
        
        :return: Dicionário com estatísticas (colisões, overflows).
        """
        return {
            "colisoes": self.colisoes,
            "overflows": self.overflows
        }