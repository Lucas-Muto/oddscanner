from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Caminho para o chromedriver (ajuste conforme necessário)
chromedriver_path = r"C:\Users\Lucas\Desktop\chromedriver-win64\chromedriver.exe"

# Configuração do serviço do ChromeDriver
service = Service(chromedriver_path)

# Inicializa o driver do Selenium
driver = webdriver.Chrome(service=service)

# Acessar a nova URL específica das odds esportivas para o Brasileirão Série A
driver.get("https://br.novibet.com/apostas-esportivas/futebol/4372606/brazil/serie-a/5909324")

# Aguardar alguns segundos para a página carregar completamente
time.sleep(5)

# Clicar no botão "ENTRAR" no primeiro pop-up (se necessário)
try:
    entrar_button = driver.find_element(By.CLASS_NAME, "registerOrLogin_sectionButtonLogin")
    entrar_button.click()
    print("Botão 'ENTRAR' clicado com sucesso!")
    time.sleep(2)
except Exception as e:
    print(f"Erro ao clicar no botão 'ENTRAR': {e}")

# Preencher o e-mail e a senha no modal de login
try:
    email_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'].input_form")
    email_field.send_keys("contatolucasmuto@gmail.com")

    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password'].input_form")
    password_field.send_keys("Jopest78")

    time.sleep(2)

    # Localizar e clicar no botão "Entrar"
    login_button = driver.find_element(By.XPATH, "//button[@class='button primary extraLarge']")
    login_button.click()
    print("Login realizado com sucesso!")
    time.sleep(5)
except Exception as e:
    print(f"Erro ao tentar preencher o formulário de login: {e}")

# Fechar o modal de boas-vindas após o login
try:
    close_modal_button = driver.find_element(By.CLASS_NAME, "noDepositors_closeButton")
    close_modal_button.click()
    print("Modal de boas-vindas fechado com sucesso!")
    time.sleep(2)
except Exception as e:
    print(f"Erro ao fechar o modal de boas-vindas: {e}")

# Capturar os cards das partidas na aba de competições específicas
try:
    # Esperar até que os cards estejam visíveis
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.eventEuro.u-flexColumn.u-flexYCenter.card")))
    cards = driver.find_elements(By.CSS_SELECTOR, "div.eventEuro.u-flexColumn.u-flexYCenter.card")
    print(f"Total de partidas encontradas: {len(cards)}")

    # Para cada card, extrair as informações de campeonato, times, odds, data e hora
    for card in cards:
        try:
            # Capturar o nome do campeonato e rodada
            competition_info = card.find_element(By.CLASS_NAME, "u-flex.u-flexYCenter.competitionLanding_competitionInfo").text.strip()

            # Capturar os times
            teams = card.find_elements(By.CLASS_NAME, "competitor")
            if len(teams) >= 2:
                team1 = teams[0].text.strip()
                team2 = teams[1].text.strip()
            else:
                print(f"Não foi possível capturar os times para uma das partidas.")
                continue

            # Capturar a data e hora da partida
            date_time = card.find_element(By.CLASS_NAME, "eventEuro_startTime").text.strip()

            # Capturar as odds de vitória, empate e derrota
            odds_container = card.find_element(By.CLASS_NAME, "marketDisplay")
            odds = odds_container.find_elements(By.CLASS_NAME, "marketBetItem_price")

            if len(odds) >= 3:
                odd_victory = odds[0].text.strip()
                odd_draw = odds[1].text.strip()
                odd_loss = odds[2].text.strip()

                # Imprimir as informações da partida e odds
                print(f"Campeonato: {competition_info}")
                print(f"Partida: {team1} vs {team2}")
                print(f"Data e Hora: {date_time}")
                print(f"Odd Vitória {team1}: {odd_victory}")
                print(f"Odd Empate: {odd_draw}")
                print(f"Odd Vitória {team2}: {odd_loss}")
                print("-----------------------------")
            else:
                print(f"Erro: Não foi possível encontrar as odds completas para a partida {team1} vs {team2}.")
        except Exception as e:
            print(f"Erro ao capturar as informações da partida: {e}")
except Exception as e:
    print(f"Erro ao localizar os cards das partidas: {e}")

# Fechar o navegador após a extração
driver.quit()
