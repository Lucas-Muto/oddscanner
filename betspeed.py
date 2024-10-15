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

# Lista de URLs e seus respectivos títulos de campeonato
urls = [
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=WORLD&championship=Liga%20das%20Na%C3%A7%C3%B5es%20UEFA&championshipId=sr:tournament:23755", "title": "Liga das Nações UEFA"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=WORLD&championship=Campeonato%20do%20Mundo,%20Qualifica%C3%A7%C3%A3o%20CONMEBOL&championshipId=sr:tournament:295", "title": "Campeonato do Mundo - Qualificação CONMEBOL"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=Brasil&championship=Copa%20do%20Brasil&championshipId=sr:tournament:373", "title": "Copa do Brasil"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=Brasil&championship=Brasileir%C3%A3o%20S%C3%A9rie%20A&championshipId=sr:tournament:325", "title": "Brasileirão Série A"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=Inglaterra&championship=Premier%20League&championshipId=sr:tournament:17", "title": "Premier League"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=Espanha&championship=La%20Liga&championshipId=sr:tournament:8", "title": "La Liga"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=It%C3%A1lia&championship=S%C3%A9rie%20A&championshipId=sr:tournament:23", "title": "Série A - Itália"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=Alemanha&championship=Bundesliga&championshipId=sr:tournament:35", "title": "Bundesliga"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=WORLD&championship=Copa%20Libertadores&championshipId=sr:tournament:384", "title": "Copa Libertadores"},
    {"url": "https://www.betspeed.com/home/events-area/s/SC?country=WORLD&championship=Ta%C3%A7a%20Sul-Americana&championshipId=sr:tournament:480", "title": "Taça Sul-Americana"}
]

# Criar o arquivo de saída
output_file = open("betspeed.txt", "w", encoding="utf-8")

# Função para processar cada URL
def scrape_betspeed(url_info, first_url=False):
    url = url_info["url"]
    championship_title = url_info["title"]

    try:
        # Abrir a URL
        driver.get(url)
        time.sleep(5)  # Esperar carregar a página

        # Fechar os modais apenas na primeira vez
        if first_url:
            # Fechar o primeiro modal
            try:
                close_modal_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[mat-dialog-close]"))
                )
                close_modal_button.click()
            except Exception as e:
                output_file.write(f"Erro ao fechar o primeiro modal: {e}\n")

            # Fechar o modal de cookies
            try:
                cookies_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Permitir apenas cookies necessários')]"))
                )
                cookies_button.click()
            except Exception as e:
                output_file.write(f"Erro ao fechar o modal de cookies: {e}\n")

        # Verificar se há jogos disponíveis
        try:
            # Capturar todas as datas na página
            match_dates = driver.find_elements(By.XPATH, "//span[@fxlayout='column' and contains(text(),'/')]")
            match_containers = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.event-body.ng-star-inserted"))
            )

            # Iterar sobre as datas e os jogos
            for date_index, date_element in enumerate(match_dates):
                date_text = date_element.text

                # Obter os jogos associados à data corrente
                games_for_date = match_containers[date_index::len(match_dates)]

                for match in games_for_date:
                    team1 = match.find_element(By.XPATH, ".//div[contains(@class, 'margin-name-5')]/span").text
                    team2 = match.find_element(By.XPATH, ".//div[contains(@class, 'event-name')]/span").text

                    try:
                        odds_container = match.find_element(By.CSS_SELECTOR, "div.odds-area")
                        odds_buttons = odds_container.find_elements(By.CSS_SELECTOR, "button.center")

                        if len(odds_buttons) == 3:
                            odd_team1 = odds_buttons[0].find_element(By.XPATH, ".//span").text
                            odd_draw = odds_buttons[1].find_element(By.XPATH, ".//span").text
                            odd_team2 = odds_buttons[2].find_element(By.XPATH, ".//span").text

                            # Formatar e armazenar os dados no arquivo
                            output_file.write(f"{championship_title}\n")
                            output_file.write(f"Data: {date_text}\n")  # Mantém a data correta no arquivo
                            output_file.write(f"[ {team1} vs {team2} ]\n")
                            output_file.write(f"Vitória {team1}: ODD {odd_team1}\n")
                            output_file.write(f"Empate: ODD {odd_draw}\n")
                            output_file.write(f"Vitória {team2}: ODD {odd_team2}\n")
                            output_file.write("-" * 35 + "\n")

                    except Exception as e:
                        output_file.write(f"Erro ao extrair as ODDS para o jogo {team1} vs {team2}: {e}\n")

        except Exception as e:
            output_file.write(f"Erro ao extrair as datas e os jogos: {e}\n")

    except Exception as e:
        output_file.write(f"Erro ao processar a URL {url}: {e}\n")

# Processar todas as URLs (primeira vez fecha modais)
for index, url_info in enumerate(urls):
    scrape_betspeed(url_info, first_url=(index == 0))

# Fechar o navegador e o arquivo
driver.quit()
output_file.close()

print("Dados extraídos e salvos com sucesso.")
