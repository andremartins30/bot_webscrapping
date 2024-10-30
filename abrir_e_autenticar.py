import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess
import os
import sys

# Caminho para o Chrome
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Diretório para o perfil do Chrome
user_data_dir = "C:/path/to/chrome-profile"

# Comando para iniciar o Chrome com depuração remota
command = [chrome_path, f"--remote-debugging-port=9222", f"--user-data-dir={user_data_dir}"]

# Iniciar o Chrome
subprocess.Popen(command)

time.sleep(2)  # Aguardar 5 segundos para o Chrome iniciar


# Configurar as opções do Chrome para conectar à sessão existente
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") 

script_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(script_dir, 'chromedriver.exe')

# Caminho para o ChromeDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

print("Conectado à sessão existente.")

# Acessa a página de login
driver.get('https://valentinatelefonica.my.site.com/s/busca-por-linha')

# Mensagem para informar ao usuário que ele deve autenticar manualmente
print("Por favor, faça o login manualmente e pressione Enter aqui quando terminar.")

# Aguardar o usuário pressionar Enter após autenticar
input("Pressione Enter quando estiver autenticado...")

print("Se a autenticação foi concluida. Você pode executar o script de consulta.")