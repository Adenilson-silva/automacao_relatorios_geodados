from processador import gerar_relatorio
import tkinter as tk
from tkinter import filedialog, ttk, Toplevel, Label, Frame, Entry, Button
import threading

def criar_interface(janela):

    fonte_titulo = ("Segoe UI", 12, "bold")
    fonte_padrao = ("Segoe UI", 9)

    # Função para selecionar arquivo .shp
    def selecionar_arquivo_shp():
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos Shapefile", "*.shp")])
        if caminho:
            entrada_shp.configure(state="normal")
            entrada_shp.delete(0, 'end')  # limpa o campo antes
            entrada_shp.insert(0, caminho)  # insere o caminho do arquivo
            verificar_campos()

    # Função para selecionar arquivo .json
    def selecionar_arquivo_json():
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
        if caminho:
            entrada_json.configure(state="normal")
            entrada_json.delete(0, 'end')  # limpa o campo antes
            entrada_json.insert(0, caminho)  # insere o caminho do arquivo
            verificar_campos()

    # Função para o diretorio que o relatório será salvo
    def selecionar_pasta():
        caminho = filedialog.askdirectory()
        if caminho:
            entrada_pasta.configure(state="normal")
            entrada_pasta.delete(0, 'end')  # limpa o campo antes
            entrada_pasta.insert(0, caminho)  # insere o caminho do arquivo
            verificar_campos()

    def mostrar_modal_processo():
        modal = Toplevel()
        modal.title("Processando")
        modal.resizable(False, False)
        modal.grab_set()
        janela.update_idletasks()  
        largura_modal = 250
        altura_modal = 90
        largura_janela = janela.winfo_width()
        altura_janela = janela.winfo_height()
        x_janela = janela.winfo_x()
        y_janela = janela.winfo_y()
        pos_x = x_janela + (largura_janela // 2) - (largura_modal // 2)
        pos_y = y_janela + (altura_janela // 2) - (altura_modal // 2)
        modal.geometry(f"{largura_modal}x{altura_modal}+{pos_x}+{pos_y}")
        Label(modal, text="Gerando relatório automático...\nPor favor, aguarde.", font=fonte_padrao).pack(expand=True, pady=20)
        return modal
    
    
    def mostrar_modal_sucesso():
        modal = Toplevel()
        modal.title("Sucesso")
        modal.resizable(False, False)
        modal.grab_set()
        janela.update_idletasks()
        largura_modal = 250
        altura_modal = 90
        largura_janela = janela.winfo_width()
        altura_janela = janela.winfo_height()
        x_janela = janela.winfo_x()
        y_janela = janela.winfo_y()
        pos_x = x_janela + (largura_janela // 2) - (largura_modal // 2)
        pos_y = y_janela + (altura_janela // 2) - (altura_modal // 2)
        modal.geometry(f"{largura_modal}x{altura_modal}+{pos_x}+{pos_y}")
        Label(modal, text="Relatório gerado com sucesso!", font=fonte_padrao).pack(pady=(20, 10))
        botao_ok = Button(modal, text="OK", width=10, command=modal.destroy)
        botao_ok.pack(pady=(0, 10))


    def gerar_em_thread(modal, caminho_shp, pasta_saida, caminho_json, projeto, dataset, tabela):
        try:
            gerar_relatorio(caminho_shp, pasta_saida, caminho_json, projeto, dataset, tabela)
        finally:
            modal.destroy()
            mostrar_modal_sucesso() 
            
    # Função executada após clique no botão Gerar relatório
    def ao_clicar_gerar():
        caminho_shp = entrada_shp.get()
        pasta_saida = entrada_pasta.get()
        caminho_json = entrada_json.get()
        projeto = entrada_projeto.get()
        dataset = entrada_dataset.get()
        tabela = entrada_tabela.get()
        modal = mostrar_modal_processo()
        thread = threading.Thread(target=gerar_em_thread, args=(modal, caminho_shp, pasta_saida, caminho_json, projeto, dataset, tabela))
        thread.start()


    # Função para verificar se todos os campos obrigatórios foram preenchidos e liberar o botão Gerar Relatório
    def verificar_campos(*args):
        if (entrada_shp.get().strip()
            and entrada_pasta.get().strip() 
            and entrada_json.get().strip()
            and entrada_projeto.get().strip() 
            and entrada_dataset.get().strip() 
            and entrada_tabela.get().strip()
            ):
            botao.config(state="normal")
        else:
            botao.config(state="disabled")


    janela.geometry("850x280")
    janela.title("Automatização de Relatórios Utilizando Dados GIS Vetoriais") 
    janela.resizable(False, False)
    
    abas = ttk.Notebook(janela)
    aba1 = Frame(abas)
    aba2 = Frame(abas)
    abas.add(aba1, text="Relatório")
    abas.add(aba2, text="Configuração BigQuery")
    abas.pack(expand=1, fill="both")


    # ---------------------------------------------- Aba 1 ----------------------------------------------
    titulo = Label(aba1, text="Relatório Automático", font=fonte_titulo, anchor="center", justify="center")
    titulo.grid(column=0, row=0, columnspan=5, pady=15, sticky="ew")

    label_arquivo = Label(aba1, text="Selecione o arquivo shapefile*:", font=fonte_padrao)
    label_arquivo.grid(column=1, row=3, padx=(40, 0), pady=5, sticky="w")
    entrada_shp = Entry(aba1, width=90)
    entrada_shp.grid(column=2, row=3)
    entrada_shp.bind("<KeyRelease>", verificar_campos)
    botao_selecionar_shp = Button(aba1, text="...", command=selecionar_arquivo_shp)
    botao_selecionar_shp.grid(column=3, row=3, padx=10)

    label_diretorio = Label(aba1, text="Salvar relatório em*:", font=fonte_padrao)
    label_diretorio.grid(column=1, row=5, padx=(40, 0), pady=5, sticky="w")
    entrada_pasta = Entry(aba1, width=90)
    entrada_pasta.grid(column=2, row=5)
    entrada_pasta.bind("<KeyRelease>", verificar_campos)
    botao_selecionar_diretorio = Button(aba1, text="...", command=selecionar_pasta)
    botao_selecionar_diretorio.grid(column=3, row=5, padx=10)

    botao = Button(aba1, text="Gerar relatório", font=fonte_padrao, width=20, command=ao_clicar_gerar, state="disabled")
    botao.grid(column=2, row=6, pady=(10, 5), sticky="ew")

    botao_cancelar = Button(aba1, text="Cancelar", font=fonte_padrao, width=20, command=janela.destroy)
    botao_cancelar.grid(column=2, row=7, pady=(5, 10), sticky="ew")


    #  ---------------------------------------------- Aba 2 ----------------------------------------------
    titulo = Label(aba2, text="Configuração de acesso ao BigQuery", font=fonte_titulo, anchor="center", justify="center")
    titulo.grid(column=0, row=0, columnspan=18, pady=15)

    label_arquivo = Label(aba2, text="Selecione o arquivo .json*:", font=fonte_padrao)
    label_arquivo.grid(column=1, row=3, padx=(40, 0), pady=5, sticky="w")
    entrada_json = Entry(aba2, width=90)
    entrada_json.grid(column=2, row=3)
    entrada_json.bind("<KeyRelease>", verificar_campos)
    entrada_json.insert(0, "C:\projeto III\credenciais.json")
    botao_selecionar = Button(aba2, text="...", command=selecionar_arquivo_json)
    botao_selecionar.grid(column=3, row=3, padx=10)

    label_projeto = Label(aba2, text="Projeto*:", font=fonte_padrao)
    label_projeto.grid(column=1, row=5, padx=(40, 0), pady=5, sticky="w")
    entrada_projeto = Entry(aba2, width=90)
    entrada_projeto.grid(column=2, row=5)
    entrada_projeto.insert(0, "uso-de-dados-gis-vetoriais") 
    entrada_projeto.bind("<KeyRelease>", verificar_campos)

    label_dataset = Label(aba2, text="Dataset*:", font=fonte_padrao)
    label_dataset.grid(column=1, row=6, padx=(40, 0), pady=5, sticky="w")
    entrada_dataset = Entry(aba2, width=90)
    entrada_dataset.grid(column=2, row=6)
    entrada_dataset.insert(0, "projeto_3") 
    entrada_dataset.bind("<KeyRelease>", verificar_campos)

    label_tabela = Label(aba2, text="Tabela*:", font=fonte_padrao)
    label_tabela.grid(column=1, row=7, padx=(40, 0), pady=5, sticky="w")
    entrada_tabela = Entry(aba2, width=90)
    entrada_tabela.grid(column=2, row=7)
    entrada_tabela.insert(0, "shapefile") 
    entrada_tabela.bind("<KeyRelease>", verificar_campos)
    
    botao_cancelar = Button(aba2, text="Cancelar", font=fonte_padrao, width=20, command=janela.destroy)
    botao_cancelar.grid(column=2, row=17, pady=(5, 10), sticky="ew")

   

