from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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

# Abrir a página da Betspeed (URL genérica para campeonatos)
driver.get("https://www.betspeed.com/home/events-area/s/SC?country=WORLD&championship=Liga%20das%20Na%C3%A7%C3%B5es%20UEFA&championshipId=sr:tournament:23755")

# Esperar alguns segundos para garantir que a página carregue
time.sleep(5)

# Criar o arquivo de saída
output_file = open("betspeed.txt", "w", encoding="utf-8")

# Fechar o primeiro modal (aquele com o botão mat-dialog-close)
try:
    close_modal_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[mat-dialog-close]"))
    )
    close_modal_button.click()
    output_file.write("Primeiro modal fechado.\n")
except Exception as e:
    output_file.write(f"Erro ao fechar o primeiro modal: {e}\n")

# Fechar o segundo modal (o de cookies)
try:
    cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Permitir apenas cookies necessários')]"))
    )
    cookies_button.click()
    output_file.write("Modal de cookies fechado.\n")
except Exception as e:
    output_file.write(f"Erro ao fechar o modal de cookies: {e}\n")

# Extrair o título do campeonato
try:
    championship_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.ng-star-inserted[fxlayout='column']"))
    )
    output_file.write(f"Título do campeonato: {championship_title.text}\n")
except Exception as e:
    output_file.write(f"Erro ao extrair o título do campeonato: {e}\n")

# Extrair as datas dos jogos
try:
    match_dates = driver.find_elements(By.XPATH, "//span[@fxlayout='column' and contains(text(),'/')]")
    for i, date_element in enumerate(match_dates, start=1):
        date_text = date_element.text
        output_file.write(f"Data: {date_text}\n")
except Exception as e:
    output_file.write(f"Erro ao extrair as datas dos jogos: {e}\n")

# Adiciona uma espera explícita para garantir que os jogos tenham carregado
time.sleep(5)

# Extrair os times dos jogos e as ODDS
try:
    match_containers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.event-body.ng-star-inserted"))
    )

    for match in match_containers:
        team1 = match.find_element(By.XPATH, ".//div[contains(@class, 'margin-name-5')]/span").text
        team2 = match.find_element(By.XPATH, ".//div[contains(@class, 'event-name')]/span").text

        try:
            odds_container = match.find_element(By.CSS_SELECTOR, "div.odds-area")
            odds_buttons = odds_container.find_elements(By.CSS_SELECTOR, "button.center")

            if len(odds_buttons) == 3:
                odd_team1 = odds_buttons[0].find_element(By.XPATH, ".//span").text
                odd_draw = odds_buttons[1].find_element(By.XPATH, ".//span").text
                odd_team2 = odds_buttons[2].find_element(By.XPATH, ".//span").text

                # Armazena os dados no arquivo
                output_file.write(f"[ {team1} vs {team2} ]\n")
                output_file.write(f"Vitória {team1}: ODD {odd_team1}\n")
                output_file.write(f"Empate: ODD {odd_draw}\n")
                output_file.write(f"Vitória {team2}: ODD {odd_team2}\n")
                output_file.write("-" * 35 + "\n")

        except Exception as e:
            output_file.write(f"Erro ao extrair as ODDS para o jogo {team1} vs {team2}: {e}\n")

except Exception as e:
    output_file.write(f"Erro ao extrair os times e ODDS dos jogos: {e}\n")

# Fechar o navegador
driver.quit()

# Fechar o arquivo
output_file.close()

print("Arquivo betspeed.txt criado com sucesso.")
