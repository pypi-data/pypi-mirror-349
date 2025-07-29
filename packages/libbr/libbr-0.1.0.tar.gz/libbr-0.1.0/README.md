# LibBR

**LibBR** é uma biblioteca simples de interface gráfica em Python, inspirada no estilo do PySimpleGUI, mas feita com Tkinter e 100% brasileira! 🇧🇷

## Exemplo de uso

```python
from libbr.core import Janela
from libbr.widgets import Texto, Botao

janela = Janela("Minha Janela", [
    [Texto("Bem-vindo à LibBR!")],
    [Botao("Clique!", lambda: print("Clicou!"))]
])

janela.iniciar()
