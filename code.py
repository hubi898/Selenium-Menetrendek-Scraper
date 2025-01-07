import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Települések listája
cities = [
    "Sárfimizdó", "Gersekarát", "Telekes", "Andrásfa", "Petőmihályfa", "Hegyhátszentpéter", 
    "Győrvár", "Nagymákfa", "Pácsony", "Olaszfa", "Kismákfa", "Vasvár", "Rábahídvég", 
    "Püspökmolnári", "Alsóújlak", "Kám", "Szemenye", "Egervölgy", "Csipkerek", 
    "Oszkó", "Csehimindszent", "Csehi", "Mikosszéplak", "Bérbaltavár", "Nagytilaj"
]

# Már meglévő kapcsolatok betöltése
connections_file = "szomszedsagi_lista.xlsx"
if os.path.exists(connections_file):
    existing_df = pd.read_excel(connections_file)
    existing_connections = set(
        tuple(row) for row in existing_df[["Induló hely", "Érkező hely"]].itertuples(index=False, name=None)
    )
else:
    existing_connections = set()

# Hiányzó kapcsolatok azonosítása
missing_connections = [
    (from_city, to_city) for from_city in cities for to_city in cities 
    if from_city != to_city and (from_city, to_city) not in existing_connections
]

# ChromeDriver beállítása
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://menetrendek.hu")
time.sleep(5)  # Várakozás a teljes betöltésre

# Függvények (változatlanok, csak röviden összefoglalva)
def select_city(input_id, city_name):
    # Település kiválasztása
    try:
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, input_id))
        )
        input_element.clear()
        input_element.send_keys(city_name)
        time.sleep(1)
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.search_results > ul > li.active"))
        )
        dropdown.click()
        print(f"'{city_name}' kiválasztva a {input_id} mezőben.")
    except Exception as e:
        print(f"Hiba a '{city_name}' kiválasztásakor: {e}")

def click_search_button():
    # Keresés gombra kattintás
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.input_send > button"))
        )
        search_button.click()
        print("Keresés gombra kattintás sikeres.")
        return True
    except Exception as e:
        print(f"Hiba a keresés gombra kattintáskor: {e}")
        return False

def load_all_results():
    # Összes találat betöltése
    try:
        while True:
            more_results_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.all.show"))
            )
            more_results_button.click()
            time.sleep(2)  # Várakozás az új találatok betöltésére
    except Exception:
        pass

def check_connection():
    # Kapcsolat ellenőrzése
    try:
        time.sleep(2)
        load_all_results()
        spans = driver.find_elements(By.CSS_SELECTOR, "div.results_body span.transferNr")
        for span in spans:
            if "0 átszállás" in span.text:
                return True
        return False
    except Exception as e:
        print(f"Hiba a kapcsolat ellenőrzésekor: {e}")
        return False

def click_modify_search_button():
    # Visszalépés a keresés módosításához
    try:
        modify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.recalc"))
        )
        modify_button.click()
    except Exception as e:
        print(f"Hiba a Keresés módosítása gombra kattintáskor: {e}")

# Dátum és idő beállítása az "Egész nap" opció kiválasztásával


# Szomszédsági lista feltöltése
connections = []
if os.path.exists(connections_file):
    connections = pd.read_excel(connections_file).values.tolist()

# Kapcsolatok ellenőrzése
for from_city, to_city in missing_connections:
    select_city("route_from", from_city)
    select_city("route_to", to_city)
    if click_search_button():
        connection_status = "Van kapcsolat" if check_connection() else "Nincs kapcsolat"
        connections.append([from_city, to_city, connection_status])
        df = pd.DataFrame(connections, columns=["Induló hely", "Érkező hely", "Kapcsolat"])
        df.to_excel(connections_file, index=False)
        click_modify_search_button()
    time.sleep(3)

# Böngésző bezárása
driver.quit()
