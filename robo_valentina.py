import os
import threading
import tkinter as tk
from tkinter import ttk
import sys
import importlib.util
import tkinter.messagebox as messagebox
import pandas as pd
import tkinter.filedialog as filedialog
from datetime import datetime

# Variáveis globais para armazenar as referências dos widgets
input_cpfs = None
input_cpfs_endereco = None
loading_label = None
loading_label_endereco = None
progress_bar = None
janela = None  # Variável global para a janela
logs = None  # Variável global para o campo de logs
logs_endereco = None
btn_carregar_ofertas = None  # Variável global para o botão de carregar ofertas
btn_carregar_financeiro = None  # Variável global para o botão de carregar financeiro

def carregar_dados_ofertas():
    try:
        df_ofertas = pd.read_csv('dados_ofertas.csv')
        salvar_arquivo(df_ofertas, "Dados de Ofertas")
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo 'dados_ofertas.csv' não foi encontrado.")

def carregar_dados_financeiro():
    try:
        df_financeiro = pd.read_csv('financeiro.csv')
        salvar_arquivo(df_financeiro, "Dados Financeiros")
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo 'financeiro.csv' não foi encontrado.")

def carregar_dados_endereco():
    try:
        df_endereco = pd.read_csv('dados_enderecos.csv')
        salvar_arquivo(df_endereco, "Dados Endereço")
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo 'dados_endereco.csv' não foi encontrado.")

def salvar_arquivo(df, titulo):
    # Obter a data e hora atual
    now = datetime.now()
    data_hora_str = now.strftime("%d-%m-%Y-%H%M")
    
    # Determinar o nome do arquivo baseado no título
    if titulo == "Dados de Ofertas":
        nome_arquivo = f"dados_ofertas_{data_hora_str}.csv"
    elif titulo == "Dados Financeiros":
        nome_arquivo = f"financeiro_{data_hora_str}.csv"
    elif titulo == "Dados Endereço":
        nome_arquivo = f"dados_endereco_{data_hora_str}.csv"
    else:
        nome_arquivo = f"arquivo_{data_hora_str}.csv"
    
    # Abrir a caixa de diálogo para escolher o local de salvamento
    caminho_diretorio = filedialog.askdirectory(title="Escolha o diretório para salvar o arquivo")
    
    if caminho_diretorio:
        caminho_arquivo = os.path.join(caminho_diretorio, nome_arquivo)
        # Salvar o DataFrame no arquivo CSV
        df.to_csv(caminho_arquivo, index=False)
        messagebox.showinfo("Sucesso", f"Os dados foram salvos em '{caminho_arquivo}'.")

def exibir_dados(df, titulo):
    # Criar uma nova janela para exibir os dados
    janela_dados = tk.Toplevel(janela)
    janela_dados.title(titulo)

    # Criar uma tabela para exibir os dados
    tabela = ttk.Treeview(janela_dados)
    tabela["columns"] = list(df.columns)
    tabela["show"] = "headings"

    # Adicionar cabeçalhos de coluna
    for coluna in df.columns:
        tabela.heading(coluna, text=coluna)

    # Adicionar linhas de dados
    for _, linha in df.iterrows():
        tabela.insert("", "end", values=list(linha))

    tabela.pack()        

def autenticar_pagina():
    # Obter o caminho absoluto do arquivo abrir_e_autenticar.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "abrir_e_autenticar.py")
    
    spec = importlib.util.spec_from_file_location("abrir_e_autenticar", script_path)
    abrir_e_autenticar = importlib.util.module_from_spec(spec)
    sys.modules["abrir_e_autenticar"] = abrir_e_autenticar
    spec.loader.exec_module(abrir_e_autenticar)

def executar_bot(script_name, input_widget, loading_label_widget, logs_widget):
    global progress_bar, btn_carregar_ofertas, btn_carregar_financeiro
    
    # Obter o caminho absoluto do arquivo script_name
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    spec = importlib.util.spec_from_file_location("consulta_cpf", script_path)
    consulta_cpf = importlib.util.module_from_spec(spec)
    sys.modules["consulta_cpf"] = consulta_cpf
    spec.loader.exec_module(consulta_cpf)
    
    # Verificar se os botões foram definidos
    if btn_carregar_ofertas is not None and btn_carregar_financeiro is not None:
        btn_carregar_ofertas.config(state=tk.DISABLED)
        btn_carregar_financeiro.config(state=tk.DISABLED)
    else:
        raise NameError("Os botões btn_carregar_ofertas e btn_carregar_financeiro não foram definidos.")
    
    # Ler o conteúdo da caixa de texto e remover espaços em branco e novas linhas
    cpfs_text = input_widget.get("1.0", tk.END).strip().replace(" ", "").replace("\n", "")
    
    # Verificar se o comprimento total do texto é múltiplo de 11
    if len(cpfs_text) % 11 != 0:
        raise ValueError("O texto inserido não é um múltiplo de 11 caracteres. Verifique os CPFs inseridos.")
    
    # Dividir o texto em blocos de 11 caracteres
    cpfs = [cpfs_text[i:i+11] for i in range(0, len(cpfs_text), 11)]
    
    # Filtrar blocos que não sejam exatamente 11 caracteres (caso haja algum erro de entrada)
    cpfs = [cpf for cpf in cpfs if len(cpf) == 11]
    
    # Verificar se a lista de CPFs não está vazia
    if not cpfs:
        raise ValueError("Nenhum CPF válido encontrado.")
    
    # Mostrar o indicador de carregamento
    loading_label_widget.config(text="Carregando...")
    
    # Função para executar o bot em um thread separado
    def run_bot():
        try:
            log_message(f"Iniciando consulta para {len(cpfs)} CPFs", logs_widget)
            consulta_cpf.run_and_save_to_dataframe(cpfs)  # Passar a lista completa de CPFs
            log_message("Consulta concluída para todos os CPFs.", logs_widget)
            messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")
        except Exception as e:
            log_error(f"Erro durante a execução: {e}", logs_widget)
            messagebox.showerror("Erro", str(e))
        finally:
            # Esconder o indicador de carregamento
            loading_label_widget.config(text="")
            if progress_bar is not None:
                progress_bar['value'] = 0  # Resetar a barra de progresso
            if btn_carregar_ofertas is not None and btn_carregar_financeiro is not None:
                btn_carregar_ofertas.config(state=tk.NORMAL)
                btn_carregar_financeiro.config(state=tk.NORMAL)
    # Iniciar o thread
    threading.Thread(target=run_bot).start()

def log_message(message, logs_widget):
    logs_widget.config(state=tk.NORMAL)
    logs_widget.insert(tk.END, message + "\n")
    logs_widget.config(state=tk.DISABLED)
    logs_widget.yview(tk.END)  # Rolagem automática para o final
    janela.update_idletasks()  # Atualizar a interface gráfica

def log_error(message, logs_widget):
    logs_widget.config(state=tk.NORMAL)
    logs_widget.insert(tk.END, "Erro: " + message + "\n")
    logs_widget.config(state=tk.DISABLED)
    logs_widget.yview(tk.END)  # Rolagem automática para o final
    janela.update_idletasks()  # Atualizar a interface gráfica

# Função para iniciar a janela
def iniciar_janela():
    global input_cpfs, input_cpfs_endereco, loading_label, loading_label_endereco, progress_bar, janela, logs, logs_endereco, btn_carregar_ofertas, btn_carregar_financeiro  # Declarar as variáveis como global para poder modificá-las
    
    # Criação da janela
    janela = tk.Tk()
    janela.title("Robô Valentina")
    
    # Definindo o tamanho da janela
    janela.geometry("550x530")

    # Criando o widget Notebook para as abas
    notebook = ttk.Notebook(janela)
    notebook.pack(fill='both', expand=True)

    # Criando o frame para a aba "Dados+Financeiro"
    frame_financeiro = tk.Frame(notebook)
    notebook.add(frame_financeiro, text="Dados Financeiro")

    # Criando o frame para a aba "Dados+Endereço"
    frame_endereco = tk.Frame(notebook)
    notebook.add(frame_endereco, text="Dados Endereço")

    # Configuração dos widgets para a aba "Dados+Financeiro"
    label_cpf_financeiro = tk.Label(frame_financeiro, text="Inserir CPFs")
    label_cpf_financeiro.grid(row=0, column=0, columnspan=2, pady=10)
    input_cpfs = tk.Text(frame_financeiro, height=10, width=50)
    input_cpfs.insert(tk.END, "Insira os CPFs aqui, um por linha, sem traços, pontos ou aspas.")
    input_cpfs.grid(row=1, column=0, columnspan=2, pady=10)
        
    label_logs_financeiro = tk.Label(frame_financeiro, text="Logs")
    label_logs_financeiro.grid(row=2, column=0, columnspan=2, pady=5)
    
    logs = tk.Text(frame_financeiro, height=5, width=50, state=tk.DISABLED)
    logs.grid(row=3, column=0, columnspan=2, pady=10)

    loading_label = tk.Label(frame_financeiro, text="", fg="red")
    loading_label.grid(row=4, column=0, columnspan=2, pady=5)

    btn_autenticar = tk.Button(frame_financeiro, text="Autenticar Página", width=20, command=autenticar_pagina)
    btn_autenticar.grid(row=6, column=0, padx=50, pady=10)

    btn_executar = tk.Button(frame_financeiro, text="Executar Robô", width=20, command=lambda: executar_bot("consulta_cpf.py", input_cpfs, loading_label, logs))
    btn_executar.grid(row=6, column=1, padx=50, pady=10)

    btn_carregar_ofertas = tk.Button(frame_financeiro, text="Salvar Dados de Ofertas", width=20, command=carregar_dados_ofertas)
    btn_carregar_ofertas.grid(row=7, column=0, padx=60, pady=20)

    btn_carregar_financeiro = tk.Button(frame_financeiro, text="Salvar Dados Financeiros", width=20, command=carregar_dados_financeiro)
    btn_carregar_financeiro.grid(row=7, column=1, padx=60, pady=20)

    # Configuração dos widgets para a aba "Dados+Endereço"
    label_cpf_endereco = tk.Label(frame_endereco, text="Inserir CPFs")
    label_cpf_endereco.grid(row=0, column=0, columnspan=2, pady=10)
    input_cpfs_endereco = tk.Text(frame_endereco, height=10, width=50)
    input_cpfs_endereco.insert(tk.END, "Insira os CPFs aqui, um por linha, sem traços, pontos ou aspas.")
    input_cpfs_endereco.grid(row=1, column=0, columnspan=2, pady=10)
    
    label_logs_endereco = tk.Label(frame_endereco, text="Logs")
    label_logs_endereco.grid(row=2, column=0, columnspan=2, pady=5)
    
    logs_endereco = tk.Text(frame_endereco, height=5, width=50, state=tk.DISABLED)
    logs_endereco.grid(row=3, column=0, columnspan=2, pady=10)

    loading_label_endereco = tk.Label(frame_endereco, text="", fg="red")
    loading_label_endereco.grid(row=4, column=0, columnspan=2, pady=5)

    btn_autenticar_endereco = tk.Button(frame_endereco, text="Autenticar Página", width=20, command=autenticar_pagina)
    btn_autenticar_endereco.grid(row=6, column=0, padx=50, pady=10)

    btn_executar_endereco = tk.Button(frame_endereco, text="Executar Robô", width=20, command=lambda: executar_bot("consulta_cpf_endereco.py", input_cpfs_endereco, loading_label_endereco, logs_endereco))
    btn_executar_endereco.grid(row=6, column=1, padx=50, pady=10)

    btn_carregar_ofertas_endereco = tk.Button(frame_endereco, text="Salvar Dados de Ofertas", width=20, command=carregar_dados_ofertas)
    btn_carregar_ofertas_endereco.grid(row=7, column=0, padx=60, pady=20)

    btn_carregar_financeiro_endereco = tk.Button(frame_endereco, text="Salvar Dados Endereço", width=20, command=carregar_dados_endereco)
    btn_carregar_financeiro_endereco.grid(row=7, column=1, padx=60, pady=20)
    
    # Iniciar a janela principal
    janela.mainloop()

# Chamando a função para rodar a aplicação
iniciar_janela()