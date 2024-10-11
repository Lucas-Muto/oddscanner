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

# Acessar a URL das odds esportivas para o Brasileirão Série A
driver.get("https://br.novibet.com/apostas-esportivas/futebol/4372606/brazil/serie-a/5909324")

# Esperar alguns segundos para a página carregar completamente
time.sleep(5)

# Fechar o modal se aparecer
try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'registerOrLogin_closeButton')]"))
    )
    close_button.click()
    print("Modal fechado com sucesso!")

    # Clicar na aba "Partidas" usando XPath com o texto "Partidas"
    try:
        partidas_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'couponSelections_subItem') and contains(., 'Partidas')]"))
        )
        partidas_tab.click()
        print("Aba 'Partidas' clicada com sucesso!")
    except Exception as e:
        print(f"Erro ao clicar na aba 'Partidas': {e}")

    # Aguardar as partidas serem carregadas
    time.sleep(3)  # Ajuste se necessário para garantir o carregamento completo

    # Localizar todos os containers de partidas
    containers = driver.find_elements(By.CLASS_NAME, "sportsCompetitionEvents_event")

    # Iterar sobre os containers e capturar os nomes dos times, horário e odds
    for container in containers:
        # Capturar a data e o horário do jogo
        try:
            match_time = container.find_element(By.CLASS_NAME, "event_startTime").text.strip()
        except Exception as e:
            match_time = "Data/Hora indisponível"
            print(f"Erro ao capturar data e horário: {e}")

        # Capturar os dois times que estão se enfrentando
        teams = container.find_elements(By.CLASS_NAME, "competitor")
        if len(teams) == 2:
            home_team = teams[0].text.strip()
            away_team = teams[1].text.strip()

            # Exibir a data, hora e os times
            print(f"{match_time}")
            print(f"[ {home_team} vs {away_team} ]")

            # Agora capturar as odds (resultado final: 1, X, 2)
            odds_container = container.find_element(By.XPATH, ".//div[contains(@class, 'marketDisplay')]")
            odds = odds_container.find_elements(By.CLASS_NAME, "marketBetItem_price")

            if len(odds) >= 3:
                odd_home_win = odds[0].text.strip()  # ODD do time 1
                odd_draw = odds[1].text.strip()      # ODD do empate
                odd_away_win = odds[2].text.strip()  # ODD do time 2

                # Exibir as odds
                print(f"Vitória {home_team}: ODD {odd_home_win}")
                print(f"Empate: ODD {odd_draw}")
                print(f"Vitória {away_team}: ODD {odd_away_win}")
            else:
                print(f"Erro ao capturar odds para a partida {home_team} vs {away_team}.")

            # Adicionar separador entre partidas
            print("-----------------------------------")
        else:
            print("Erro ao capturar times.")

    # Pausar por 10 segundos para visualização
    time.sleep(10)
    print("Esperado 10 segundos após capturar as partidas e odds.")

except Exception as e:
    print(f"Erro ao fechar o modal ou processar a página: {e}")

# Continuar com a navegação para a página desejada ou encerrar
print("Processo concluído. Aguardando mais instruções.")
