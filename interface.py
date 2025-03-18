import tkinter as tk
from tkinter import messagebox
from classes import Tabela, Tupla, HashIndex

class HashIndexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Índice Hash")
        
        self.tabela = Tabela()
        self.hash_index = None
        
        self.criar_interface()

    def criar_interface(self):
        # Entrada para o tamanho da página
        tk.Label(self.root, text="Tamanho da Página:").grid(row=0, column=0)
        self.entry_tamanho_pagina = tk.Entry(self.root)
        self.entry_tamanho_pagina.grid(row=0, column=1)
        
        # Botão para carregar arquivo
        tk.Button(self.root, text="Carregar Arquivo", command=self.carregar_arquivo).grid(row=1, column=0, columnspan=2)
        
        # Entrada para a chave de busca
        tk.Label(self.root, text="Chave de Busca:").grid(row=2, column=0)
        self.entry_chave_busca = tk.Entry(self.root)
        self.entry_chave_busca.grid(row=2, column=1)
        
        # Botão para buscar usando índice hash
        tk.Button(self.root, text="Buscar com Índice Hash", command=self.buscar_indice_hash).grid(row=3, column=0)
        
        # Botão para fazer table scan
        tk.Button(self.root, text="Table Scan", command=self.table_scan).grid(row=3, column=1)
        
        # Botão para limpar resultados
        tk.Button(self.root, text="Limpar", command=self.limpar_resultados).grid(row=3, column=2)
        
        # Área para mostrar resultados
        self.text_resultados = tk.Text(self.root, height=10, width=50)
        self.text_resultados.grid(row=4, column=0, columnspan=3)

    def carregar_arquivo(self):
        try:
            tamanho_pagina = int(self.entry_tamanho_pagina.get())
        except ValueError:
            messagebox.showerror("Erro", "Tamanho da página deve ser um número inteiro.")
            return
        
        try:
            with open("words.txt", "r") as file:
                for linha in file:
                    chave = linha.strip()
                    tupla = Tupla(chave, chave)
                    self.tabela.adicionar_tupla(tupla, tamanho_pagina)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo 'words.txt' não encontrado.")
            return
        
        # Criar páginas e buckets
        nr = len(self.tabela.tuplas)
        fr = 10  # Exemplo, pode ser ajustado
        nb = nr // fr + 1
        self.hash_index = HashIndex(nb, fr)
        
        for i, pagina in enumerate(self.tabela.paginas):
            for tupla in pagina.tuplas:
                self.hash_index.adicionar_tupla(tupla, i)
        
        messagebox.showinfo("Sucesso", "Arquivo carregado e índice construído!")

    def buscar_indice_hash(self):
        chave = self.entry_chave_busca.get()
        if not chave:
            messagebox.showwarning("Aviso", "Digite uma chave de busca.")
            return
        
        if not self.hash_index:
            messagebox.showwarning("Aviso", "O índice hash ainda não foi construído.")
            return
        
        # Busca a tupla usando o índice hash
        tupla, pagina, custo = self.hash_index.buscar_tupla(chave)
        
        # Exibe o resultado na interface gráfica
        self.text_resultados.insert(tk.END, f"Buscar com Índice Hash:\n")
        if tupla:
            self.text_resultados.insert(tk.END, f"Chave encontrada: {tupla.dados}\n")
            self.text_resultados.insert(tk.END, f"Página: {pagina}\n")
            self.text_resultados.insert(tk.END, f"Custo: {custo} páginas lidas\n")
        else:
            self.text_resultados.insert(tk.END, "Chave não encontrada.\n")
        self.text_resultados.insert(tk.END, "-" * 50 + "\n")  # Separador

    def table_scan(self):
        chave = self.entry_chave_busca.get()
        if not chave:
            messagebox.showwarning("Aviso", "Digite uma chave de busca.")
            return
        
        custo = 0
        
        # Exibe o resultado na interface gráfica
        self.text_resultados.insert(tk.END, f"Table Scan:\n")
        
        # Percorre todas as páginas e tuplas
        for i, pagina in enumerate(self.tabela.paginas):
            custo += 1
            for tupla in pagina.tuplas:
                if tupla.chave == chave:
                    self.text_resultados.insert(tk.END, f"Chave encontrada na posição {i}: {tupla.dados}\n")
                    self.text_resultados.insert(tk.END, f"Página: {i}\n")
                    self.text_resultados.insert(tk.END, f"Custo: {custo} páginas lidas\n")
                    self.text_resultados.insert(tk.END, "-" * 50 + "\n")  # Separador
                    return
        
        # Se a chave não for encontrada
        self.text_resultados.insert(tk.END, "Chave não encontrada.\n")
        self.text_resultados.insert(tk.END, "-" * 50 + "\n")  # Separador

    def limpar_resultados(self):
        """
        Limpa a área de resultados.
        """
        self.text_resultados.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = HashIndexApp(root)
    root.mainloop()