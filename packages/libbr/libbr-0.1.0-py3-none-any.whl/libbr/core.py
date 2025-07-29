import tkinter as tk

class Janela:
    def __init__(self, titulo="LibBR Janela", layout=[]):
        self.janela = tk.Tk()
        self.janela.title(titulo)
        self.layout = layout
        self.widgets = []

    def construir(self):
        for linha in self.layout:
            linha_frame = tk.Frame(self.janela)
            linha_frame.pack(pady=2)
            for widget in linha:
                widget.renderizar(linha_frame)
                self.widgets.append(widget)

    def iniciar(self):
        self.construir()
        self.janela.mainloop()
