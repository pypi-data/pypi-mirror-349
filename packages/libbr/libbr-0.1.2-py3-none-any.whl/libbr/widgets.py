import tkinter as tk

class Texto:
    def __init__(self, texto):
        self.texto = texto

    def renderizar(self, master):
        label = tk.Label(master, text=self.texto)
        label.pack(side=tk.LEFT, padx=5)

class Botao:
    def __init__(self, texto, ao_clicar):
        self.texto = texto
        self.ao_clicar = ao_clicar

    def renderizar(self, master):
        botao = tk.Button(master, text=self.texto, command=self.ao_clicar)
        botao.pack(side=tk.LEFT, padx=5)
