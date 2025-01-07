from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.ksh.hu/apps/hntr.telepules?p_lang=HU&p_id=09788")

# List of cities to search
cities = ["Sárfimizdó", "Gersekarát", "Telekes", "Andrásfa", "Petőmihályfa", "Hegyhátszentpéter", 
    "Győrvár", "Nagymákfa", "Pácsony", "Olaszfa", "Kismákfa", "Vasvár", "Rábahídvég", 
    "Püspökmolnári", "Alsóújlak", "Kám", "Szemenye", "Egervölgy", "Csipkerek", 
    "Oszkó", "Csehimindszent", "Csehi", "Mikosszéplak", "Bérbaltavár", "Nagytilaj"
]  # Add more cities as needed

# Create a DataFrame to store results
results = []

for city in cities:
    # Find the search input and enter the city name
    search_box = driver.find_element(By.ID, "p_szo")
    search_box.clear()
    search_box.send_keys(city)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for the results to load
    time.sleep(3)
    
    # Click the first result from the search list
    first_result = driver.find_element(By.CSS_SELECTOR, "#searchlist-list tbody tr a")
    first_result.click()
    
    # Wait for the city page to load
    time.sleep(3)
    
    # Scrape population data (or other details)
    try:
        table = driver.find_element(By.ID, "data-cens").find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Get the population from the first row of the table
        population = rows[1].find_elements(By.TAG_NAME, "td")[1].text
        
        # Append results to the list
        results.append({"City": city, "Population": population})
    except Exception as e:
        print(f"Failed to scrape {city}: {e}")
        continue

# Convert results to DataFrame and save as Excel
df = pd.DataFrame(results)
df.to_excel('city_population.xlsx', index=False)

# Close the browser
driver.quit()
