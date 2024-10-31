from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Path to the chromedriver (adjust as needed)
chromedriver_path = r"C:\Users\Lucas\Desktop\chromedriver-win64\chromedriver.exe"

# List of URLs with corresponding titles
urls = [
    ("https://br.betano.com/sport/futebol/brasil/brasileirao-serie-a-betano/10016/", "Brasileirão - Serie A"),
    ("https://br.betano.com/en/sport/soccer/competitions/copa-libertadores/189817/", "Copa Libertadores"),
    ("https://br.betano.com/en/sport/soccer/brazil/copa-betano-do-brasil/10008/", "Copa do Brasil"),
    ("https://br.betano.com/en/sport/soccer/competitions/copa-sudamericana/189818/", "Copa Sulamericana"),
    ("https://br.betano.com/en/sport/soccer/competitions/england/1/", "Premier League"),
    ("https://br.betano.com/en/sport/soccer/spain/laliga/5/", "La Liga"),
    ("https://br.betano.com/en/sport/soccer/competitions/italy/87/?sl=1635", "Itália - Série A"),
    ("https://br.betano.com/en/sport/soccer/germany/bundesliga/216/", "Bundesliga"),
    ("https://br.betano.com/en/sport/soccer/competitions/champions-league/188566/", "Liga dos Campeões UEFA"),
    ("https://br.betano.com/en/sport/soccer/competitions/europa-league/188567/", "Liga Europa UEFA"),
]

# Function to close the modal if it appears
def close_modal_if_exists(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sb-modal__close__btn"))
        )
        close_button.click()
        print("Modal closed.")
        time.sleep(1)  # Give it a moment to fully close
    except Exception as e:
        print("No modal appeared or failed to close modal:", e)

# Function to extract match data
def extract_matches(driver):
    match_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-qa='league_page_event']")
    matches = set()  # Set to hold unique matches

    for match in match_elements:
        # Date and Time
        try:
            date_time_container = match.find_element(By.CSS_SELECTOR, "div.tw-text-n-48-slate")
            date = date_time_container.find_elements(By.TAG_NAME, "span")[0].text
            time_str = date_time_container.find_elements(By.TAG_NAME, "span")[1].text
            date_time = f"{date} {time_str}"
        except Exception:
            date_time = "N/A"

        # Teams
        try:
            teams = match.find_elements(By.CSS_SELECTOR, "div.tw-truncate.tw-text-s.tw-font-medium")
            team1 = teams[0].text if len(teams) > 0 else "N/A"
            team2 = teams[1].text if len(teams) > 1 else "N/A"
        except Exception:
            team1, team2 = "N/A", "N/A"

        # Odds
        try:
            odds = match.find_elements(By.CSS_SELECTOR, "span.tw-text-s.tw-leading-s.tw-font-bold.tw-text-tertiary.dark\\:tw-text-quartary")
            odd_team1 = odds[0].text if len(odds) > 0 else "N/A"
            odd_draw = odds[1].text if len(odds) > 1 else "N/A"
            odd_team2 = odds[2].text if len(odds) > 2 else "N/A"
        except Exception:
            odd_team1, odd_draw, odd_team2 = "N/A", "N/A", "N/A"

        # Create a tuple with match data to check for duplicates
        match_data = (
            date_time,
            team1,
            team2,
            f"Vitória {team1}: ODD {odd_team1}",
            f"Empate: ODD {odd_draw}",
            f"Vitória {team2}: ODD {odd_team2}",
        )

        matches.add(match_data)  # Add unique match data to the set
    
    return matches

# Open the file for writing
with open("betano.txt", "w", encoding="utf-8") as file:
    for url, title in urls:
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        
        close_modal_if_exists(driver)
        time.sleep(3)  # Wait 3 seconds after checking for a modal

        file.write(f"{title}\n\n")
        print(f"Processing {title}...")

        # Loop to extract data at incremental scroll positions (0.2 steps)
        all_matches = set()  # Combined unique matches for each URL
        current_scroll = 0
        while current_scroll < 1.0:
            all_matches.update(extract_matches(driver))  # Extract matches and add to the set
            driver.execute_script(f"window.scrollBy(0, document.body.scrollHeight * 0.2);")
            time.sleep(2)  # Pause to allow content to load
            current_scroll += 0.2

        # Write unique matches to file
        for match in all_matches:
            date_time, team1, team2, odd_team1, odd_draw, odd_team2 = match
            file.write(f"{date_time}\n")
            file.write(f"[ {team1} vs {team2} ]\n")
            file.write(f"{odd_team1}\n")
            file.write(f"{odd_draw}\n")
            file.write(f"{odd_team2}\n")
            file.write("-----------------------------------\n")
        file.write("\n\n")

        driver.quit()
        print(f"Finished processing {title}.\n")

print("Data successfully written to betano.txt")
