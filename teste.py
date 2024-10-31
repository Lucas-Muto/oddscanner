from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Caminho para o chromedriver (ajuste conforme necessário)
chromedriver_path = r"C:\Users\Lucas\Desktop\chromedriver-win64\chromedriver.exe"

# Configuração inicial do Chrome para evitar detecção de Selenium
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Configuração do serviço do ChromeDriver
service = Service(chromedriver_path)

# Inicializa o driver do Selenium com as opções definidas
driver = webdriver.Chrome(service=service, options=chrome_options)

# Função para fechar o modal
def fechar_modal(driver):
    try:
        modal_close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sb-modal__close__btn"))
        )
        if modal_close_button:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "sb-modal__close__btn"))).click()
            print("Modal fechado com sucesso.")
    except (TimeoutException, NoSuchElementException):
        print("Modal não encontrado ou não apareceu. Seguindo com a navegação.")

# Função para extrair o título do campeonato
def extrair_titulo_campeonato(driver):
    try:
        titulo_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.tw-font-bold"))
        )
        titulo = titulo_elemento.text
        print(f"Título do campeonato: {titulo}")
        return titulo
    except TimeoutException:
        print("Título do campeonato não encontrado.")
        return None

# Função para extrair a primeira partida
def extrair_primeira_partida(driver):
    try:
        partida_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-qa="participants"]'))
        )
        # Localiza o primeiro time
        time1_elemento = partida_elemento.find_element(By.CSS_SELECTOR, 'div.tw-flex-row.tw-items-center.tw-justify-start.tw-w-full.tw-mb-s .tw-truncate')
        time1 = time1_elemento.text
        
        # Localiza o segundo time
        time2_elemento = partida_elemento.find_element(By.CSS_SELECTOR, 'div.tw-flex-row.tw-items-center.tw-justify-start.tw-w-full:not(.tw-mb-s) .tw-truncate')
        time2 = time2_elemento.text
        
        print(f"Primeira partida: {time1} vs {time2}")
        return time1, time2
    except TimeoutException:
        print("Primeira partida não encontrada.")
        return None, None

# Função para extrair data e horário da partida usando XPath
def extrair_data_horario(driver):
    try:
        # Captura a data usando XPath fornecido
        data_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/section[2]/div[4]/div[2]/div[1]/section/div/div/div/div[2]/div[1]/div[1]/div/div[1]/div/span[1]'))
        )
        data = data_elemento.text
        
        # Captura o horário usando XPath fornecido
        horario_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/section[2]/div[4]/div[2]/div[1]/section/div/div/div/div[2]/div[1]/div[1]/div/div[1]/div/span[2]'))
        )
        horario = horario_elemento.text
        
        print(f"Data: {data}, Horário: {horario}")
        return data, horario
    except TimeoutException:
        print("Data e horário não encontrados pelo XPath.")
        return None, None

# Acessa a URL
driver.get("https://br.betano.com/sport/futebol/brasil/brasileirao-serie-a-betano/10016/")

# Chama a função para fechar o modal
fechar_modal(driver)

# Extrai o título do campeonato
titulo_campeonato = extrair_titulo_campeonato(driver)

# Extrai a primeira partida
time1, time2 = extrair_primeira_partida(driver)

# Extrai a data e o horário da partida usando XPath
data, horario = extrair_data_horario(driver)

# Exibe o resultado formatado se todos os elementos foram encontrados
if titulo_campeonato and time1 and time2 and data and horario:
    print(f"{titulo_campeonato}")
    print(f"Data: {data} {horario}")
    print(f"[ {time1} vs {time2} ]")
    print("-----------------------------------")

# Aguarda alguns segundos para garantir que a navegação foi bem-sucedida
time.sleep(3)

# Fechar o driver após a navegação
driver.quit()
