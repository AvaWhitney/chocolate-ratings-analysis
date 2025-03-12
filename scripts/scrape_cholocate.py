from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Path to your ChromeDriver (change this to your actual path)
chrome_driver_path = "C:\Program Files\Google\chromedriver-win64\chromedriver.exe"

# Initialize Selenium WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage
url = "https://flavorsofcacao.com/chocolate_database.html"
driver.get(url)

# Time to wait until the table is loaded
wait = WebDriverWait(driver, 10) 
table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@border, '1')]")))

# Get all table rows
rows = table.find_elements(By.XPATH, ".//tr[position() > 1]")

# Extract data
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")  # Get columns (skip headers)
    cols = [col.text.strip() for col in cols]  # Extract text
    if len(cols) == 10:  # Only add non-empty rows
        data.append(cols)


# Convert to DataFrame
columns = ["REF", "Company(Manufacturer)", "Company Location", "Review Date", "Country of Bean Origin", 
           "Specific Bean Origin or Bar Name", "Cocoa Percent", "Ingredients", 
           "Most Memorable Characteristics", "Rating"]
df = pd.DataFrame(data, columns=columns)



# Save to CSV
df.to_csv("chocolate_ratings.csv", index=False)

# Close the browser
driver.quit()

print("Scraping completed! Data saved as chocolate_ratings.csv")

