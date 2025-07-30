import tkinter as tk
from tkinter import messagebox
class Texto:
    def __init__(self, texto):
        self.texto = texto

    def renderizar(self, master):
        label = tk.Label(master, text=self.texto)
        label.pack(side=tk.LEFT, padx=5)
        return label

class Entrada:
    def __init__(self, largura=20, chave=None):
        self.largura = largura
        self.chave = chave
        self.entrada = None

    def renderizar(self, master):
        self.entrada = tk.Entry(master, width=self.largura)
        self.entrada.pack(side=tk.LEFT, padx=5)
        return self.entrada

    def obter_valor(self):
        return self.entrada.get()

class Botao:
    def __init__(self, texto, ao_clicar):
        self.texto = texto
        self.ao_clicar = ao_clicar

    def renderizar(self, master):
        botao = tk.Button(master, text=self.texto, command=self.ao_clicar)
        botao.pack(side=tk.LEFT, padx=5)
        return botao

class CaixaSelecao:
    def __init__(self, texto, chave=None):
        self.texto = texto
        self.chave = chave
        self.variavel = None

    def renderizar(self, master):
        self.variavel = tk.BooleanVar(master)
        checkbox = tk.Checkbutton(master, text=self.texto, variable=self.variavel)
        checkbox.pack(side=tk.LEFT, padx=5)
        return checkbox

    def obter_valor(self):
        if self.variavel:
            return self.variavel.get()
        return None
    
    
class OpcaoUnica:
    def __init__(self, texto, variavel, valor, chave=None):
        self.texto = texto
        self.variavel = variavel
        self.valor = valor
        self.chave = chave

    def renderizar(self, master):
        radio = tk.Radiobutton(master, text=self.texto, variable=self.variavel, value=self.valor)
        radio.pack(side=tk.LEFT, padx=5)
        return radio

    def obter_valor(self):
        return self.variavel.get()

class JanelaPopup:
    def __init__(self, titulo, mensagem):
        self.janela = tk.Tk()
        self.janela.withdraw()  # Oculta a janela principal
        self.mensagem = mensagem
        self.titulo = titulo
        messagebox.showinfo(self.titulo, self.mensagem)
        self.janela.destroy()