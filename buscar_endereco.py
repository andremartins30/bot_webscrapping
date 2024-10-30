from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configurações do Chrome (certifique-se de que o Chrome foi iniciado em modo de depuração)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Conectado à sessão existente.")

# Inicializar o WebDriverWait
wait = WebDriverWait(driver, 10)

def buscar_endereco():
    # Inicializar a lista de resultados
    resultados = []

    # Esperar até que o endereço seja carregado
    nome_cliente = wait.until(EC.presence_of_element_located((By.XPATH, '//h1//span//strong'))).text.strip()
    elemento_span_text = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@style, "font-size: 20px;")]'))).text.strip()
    
    # Obter todos os elementos correspondentes ao XPATH
    elementos_p = wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/c-val-billing-account-english/div/article/div[2]/vlocity_cmt-omniscript-step/div[2]/slot/vlocity_cmt-omniscript-custom-lwc[1]/slot/c-cf-val-review-customer/div/vlocity_cmt-flex-card-state[2]/div/slot/div/div[2]/vlocity_cmt-block/div/div/div/slot/div/div/c-cf-val-review-customer-body/div/vlocity_cmt-flex-card-state/div/slot/div')))
    
    # Verificar se elementos_p está vazio
    if not elementos_p:
        print("Nenhum elemento encontrado com o XPATH fornecido.")
        elemento_p_texts = []
    else:
        elemento_p_texts = [elem.text.strip() for elem in elementos_p]

        # Índices a serem removidos
        indices_to_remove = [0, 2, 4, 6, 8, 10, 12]

        # Remover os itens dos índices especificados
        for index in sorted(indices_to_remove, reverse=True):
            if index < len(elemento_p_texts):
                del elemento_p_texts[index]

        # Garantir que os elementos estejam separados por ''
        elemento_p_texts = [elem if elem else '' for elem in elemento_p_texts]

    endereco = driver.find_elements(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/c-val-billing-account-english/div/article/div[2]/vlocity_cmt-omniscript-step/div[2]/slot/vlocity_cmt-omniscript-custom-lwc[2]/slot/c-cf-val-billing-account-details-container/div/vlocity_cmt-flex-card-state/div/slot/div/div[2]/vlocity_cmt-block/div/div/div/slot/div/div[2]/vlocity_cmt-block/div/div/div/slot/div/div/c-cf-val-billing-account-address-information/div/vlocity_cmt-flex-card-state/div/slot/div/div[2]/vlocity_cmt-block/div/div/div/slot/div')

    print('Nome do cliente:', nome_cliente)
    print('Elemento span:', elemento_span_text)
    print('Elemento p:', elemento_p_texts)

    resultados.insert(1, nome_cliente)
    resultados.insert(2, elemento_span_text)
    resultados.insert(3, elemento_p_texts)

    if endereco:
        endereco_text = endereco[0].text.strip()
        resultados.insert(4, endereco_text)
        print("Endereço encontrado:", endereco_text)
    else:
        print("Endereço não encontrado.")
        resultados.insert(4, "")

    positions_to_remove = [10, 13, 14, 15, 16, 19]
    for pos in sorted(positions_to_remove, reverse=True):
        if pos < len(resultados):
            del resultados[pos]

    # driver.back()

    # time.sleep(5)

    return resultados

buscar_endereco()