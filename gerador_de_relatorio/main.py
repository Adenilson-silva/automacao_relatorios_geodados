from tkinter import * 
from ui import criar_interface
#from processador import gerar_relatorio

def main():
    # Cria a interface do usuário
    janela = Tk()
    criar_interface(janela)
    janela.mainloop()

if __name__ == "__main__":
    main()
