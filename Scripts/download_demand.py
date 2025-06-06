import os
import time
import glob
import shutil
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === PATH SETUP ===
download_dir = os.path.join(os.getcwd(), "Daily-Demand")
os.makedirs(download_dir, exist_ok=True)

# === DATE CONFIG ===
yesterday = datetime.utcnow() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")
url_date_str = yesterday.strftime("%d-%m-%Y")

# === BUILD URL ===
url = f"https://www.esios.ree.es/es/analisis/1293?vis=1&start_date={url_date_str}T00%3A00&end_date={url_date_str}T23%3A55&groupby=hour"

# === CHROME OPTIONS ===
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})

# === LAUNCH DRIVER ===
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
driver.get(url)

try:
    print("⏳ Waiting for export button...")

    # Accept cookies
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        cookie_button.click()
        print("🍪 Cookies accepted")
    except:
        print("🍪 No cookie popup")

    # Export CSV
    export_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, "export_multiple"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", export_button)
    time.sleep(1)
    export_button.click()

    csv_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='opt-ancle' and contains(text(), 'CSV')]"))
    )
    driver.execute_script("arguments[0].click();", csv_option)
    print("📄 CSV clicked, downloading...")

    # Wait for file
    time.sleep(15)

    # Find downloaded CSV
    downloaded_files = glob.glob(os.path.join(download_dir, "*.csv"))
    if downloaded_files:
        latest_file = max(downloaded_files, key=os.path.getctime)

        # Filter CSV to include only rows with the correct date
        df = pd.read_csv(latest_file, sep=";")
        df_filtered = df[df["datetime"].str.startswith(yesterday_str)]

        # Save cleaned CSV
        output_file = os.path.join(download_dir, f"{yesterday_str}.csv")
        df_filtered.to_csv(output_file, index=False, sep=";")
        os.remove(latest_file)

        print(f"✅ Cleaned CSV saved as: {output_file}")
    else:
        print("⚠️ No CSV file found to rename.")

except Exception as e:
    print("❌ Error:", e)

finally:
    driver.quit()

print(f"✅ Done. Check folder:\n📁 {download_dir}")

