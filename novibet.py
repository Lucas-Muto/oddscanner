from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import subprocess

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

# Lista de URLs dos campeonatos da América do Sul
urls_america_sul = [
    "https://br.novibet.com/apostas-esportivas/futebol/4372606/brazil/serie-a/5909324",  # Série A - Brasil
    "https://br.novibet.com/apostas-esportivas/futebol/4372606/brazil/copa-do-brasil/4381081",  # Copa do Brasil
    "https://br.novibet.com/apostas-esportivas/futebol/4372606/south-america/copa-sudamericana/4380718",  # Copa Sulamericana
    "https://br.novibet.com/apostas-esportivas/futebol/4372606/south-america/copa-libertadores/4380709"   # Copa Libertadores
]

# Lista de URLs dos campeonatos da Europa
urls_europa = [
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/champions-league/uefa-champions-league/5102048",  # Champions League
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/europa-conference-league/uefa-europa-conference-league/5102056",  # Conference League
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/europa-league/uefa-europa-league/4372887",  # Europa League
    # Novos campeonatos
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/england/premier-league/5908949",  # Premier League
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/england/fa-cup/4373735",  # FA Cup
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/spain/laliga/5909177",  # La Liga
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/spain/copa-del-rey/4375978",  # Copa del Rey
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/italy/serie-a/5909241",  # Serie A
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/italy/coppa-italia/4376102",  # Coppa Italia
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/germany/bundesliga/5909087",  # Bundesliga
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/germany/dfb-pokal/4376067",  # DFB Pokal
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/france/ligue-1/5909322",  # Ligue 1
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/france/coupe-de-france/4376257"  # Coupe de France
]

# Lista de URLs dos campeonatos de seleções
urls_selecoes = [
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/europe/uefa-nations-league/4373075",  # UEFA Nations League
    "https://brasil.novibet.com/apostas-esportivas/futebol/4372606/world/world-cup-2026/4679255"  # Copa do Mundo 2026
]

# Iniciar o conteúdo do arquivo com os títulos das regiões e o nome do site
output_content = "AMÉRICA DO SUL ( NOVIBET )\n\n"

# Função para acessar cada campeonato e coletar as informações
def scrape_championship(url, region_title):
    global output_content
    
    # Acessar a URL do campeonato
    driver.get(url)
    
    # Esperar 5 segundos para a página carregar completamente
    time.sleep(3)

    # Fechar o modal se aparecer
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'registerOrLogin_closeButton')]"))
        )
        close_button.click()
    except Exception as e:
        pass  # Se não houver modal, seguir em frente

    # Verificar se a aba "Partidas" está presente
    try:
        partidas_tab = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'couponSelections_subItem') and contains(., 'Partidas')]"))
        )
        partidas_tab.click()
    except Exception as e:
        print(f"A aba 'Partidas' não está disponível para {url}. Pulando este campeonato.")
        return  # Pular para o próximo campeonato

    # Aguardar 5 segundos para as partidas serem carregadas
    time.sleep(1)

    # Capturar o nome do campeonato e o país
    try:
        league_title = driver.find_element(By.CLASS_NAME, "couponHeaderSingle_leagueTitle").text.strip()
        league_country = driver.find_element(By.CLASS_NAME, "couponHeaderSingle_leagueSubtitle").text.strip()
        league_info = f"{league_title} ({league_country})"
    except Exception as e:
        league_info = "Campeonato/Pais não disponível"
    
    # Localizar todos os containers de partidas
    containers = driver.find_elements(By.CLASS_NAME, "sportsCompetitionEvents_event")

    # Iterar sobre os containers e capturar os nomes dos times, horário e odds
    for container in containers:
        # Capturar a data e o horário do jogo
        try:
            match_time = container.find_element(By.CLASS_NAME, "event_startTime").text.strip()
        except Exception as e:
            match_time = "Data/Hora indisponível"

        # Capturar os dois times que estão se enfrentando
        teams = container.find_elements(By.CLASS_NAME, "competitor")
        if len(teams) == 2:
            home_team = teams[0].text.strip()
            away_team = teams[1].text.strip()

            # Adicionar campeonato, data, hora e os times ao conteúdo
            output_content += f"{league_info}\n"
            output_content += f"{match_time}\n"
            output_content += f"[ {home_team} vs {away_team} ]\n"

            # Agora capturar as odds (resultado final: 1, X, 2)
            odds_container = container.find_element(By.XPATH, ".//div[contains(@class, 'marketDisplay')]")
            odds = odds_container.find_elements(By.CLASS_NAME, "marketBetItem_price")

            if len(odds) >= 3:
                odd_home_win = odds[0].text.strip()  # ODD do time 1
                odd_draw = odds[1].text.strip()      # ODD do empate
                odd_away_win = odds[2].text.strip()  # ODD do time 2

                # Adicionar as odds ao conteúdo
                output_content += f"Vitória {home_team}: ODD {odd_home_win}\n"
                output_content += f"Empate: ODD {odd_draw}\n"
                output_content += f"Vitória {away_team}: ODD {odd_away_win}\n"
                output_content += "-----------------------------------\n"
            else:
                output_content += f"Erro ao capturar odds para a partida {home_team} vs {away_team}.\n"
        else:
            output_content += "Erro ao capturar times.\n"

# Iterar sobre os links dos campeonatos da América do Sul
for url in urls_america_sul:
    scrape_championship(url, "AMÉRICA DO SUL")

# Adicionar um título para os campeonatos da Europa
output_content += "\nEUROPA ( NOVIBET )\n\n"

# Iterar sobre os links dos campeonatos da Europa
for url in urls_europa:
    scrape_championship(url, "EUROPA")

# Adicionar um título para os campeonatos de seleções
output_content += "\nSELEÇÕES ( NOVIBET )\n\n"

# Iterar sobre os links dos campeonatos de seleções
for url in urls_selecoes:
    scrape_championship(url, "SELEÇÕES")

# Fechar o driver no final
driver.quit()

# Salvar o conteúdo em um arquivo de texto
with open("novibet.txt", "w", encoding="utf-8") as file:
    file.write(output_content)

print("Arquivo 'novibet.txt' gerado com sucesso.")
