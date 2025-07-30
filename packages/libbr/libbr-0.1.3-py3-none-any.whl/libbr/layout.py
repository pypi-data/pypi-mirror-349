import tkinter as tk

class Layout:
    def __init__(self, titulo="LibBR", tamanho=(400, 300), cor_fundo="white", elementos=[]):
        self.titulo = titulo
        self.largura, self.altura = tamanho
        self.cor_fundo = cor_fundo
        self.elementos = elementos
        self.valores = {}
        self.widgets_por_chave = {}
        self.root = None

    def rodar(self):
        self.root = tk.Tk()
        self.root.title(self.titulo)
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.configure(bg=self.cor_fundo)

        for linha in self.elementos:
            frame = tk.Frame(self.root, bg=self.cor_fundo)
            frame.pack(pady=5)

            for elemento in linha:
                widget = elemento.renderizar(frame)

                if hasattr(elemento, "chave") and elemento.chave:
                    self.widgets_por_chave[elemento.chave] = elemento

        self.root.mainloop()

    def obter_valores(self):
        for chave, widget in self.widgets_por_chave.items():
            if hasattr(widget, "obter_valor"):
                self.valores[chave] = widget.obter_valor()
        return self.valores
