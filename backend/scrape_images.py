import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs

# --- KONFIGURASI SCRAPER ---
HERO_NAME = 'Layla' 
SEARCH_TERM = f'{HERO_NAME} mobile legends' 
OUTPUT_DIR = f'../dataset/{HERO_NAME}' 
MAX_IMAGES = 150 # Target jumlah gambar yang ingin diunduh

# 1. Persiapan Folder
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Folder '{OUTPUT_DIR}' berhasil dibuat.")
else:
    print(f"Folder '{OUTPUT_DIR}' sudah ada.")

# 2. Pengaturan Selenium
chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

def scrape_pinterest(search_term, output_folder, max_images):
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"❌ GAGAL MEMULAI WEBDRIVER. Pastikan Chrome terinstal. Error: {e}")
        return

    pinterest_url = f'https://id.pinterest.com/search/pins/?q={search_term.replace(" ", "%20")}'
    driver.get(pinterest_url)
    print(f"Mengunjungi: {pinterest_url}")

    downloaded_count = 0
    image_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    print("Memulai scrolling untuk memuat konten dinamis...")
    while downloaded_count < max_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        try:
            elements = driver.find_elements(By.XPATH, "//div[@data-grid-item='true']//img")
        except:
            print("❌ Pop-up Login mungkin muncul. Coba jalankan tanpa mode headless.")
            break
            
        for img in elements:
            src = img.get_attribute('src')
            if src and '236x' in src:
                full_src = src.replace('236x', 'originals')
                image_urls.add(full_src)
            if len(image_urls) >= max_images + 5: 
                break
        
        if new_height == last_height:
            print("Pencarian mencapai batas scroll Pinterest.")
            break
            
        last_height = new_height
        print(f"URL ditemukan: {len(image_urls)}. Target: {max_images}")

    driver.quit()
    print("WebDriver ditutup. Memulai pengunduhan...")

    # --- TAHAP PENGUNDUHAN ---
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in list(image_urls)[:max_images]:
        try:
            img_response = requests.get(url, headers=headers, timeout=15)
            img_response.raise_for_status()
            url_path = urlparse(url).path
            img_name = os.path.basename(url_path)
            
            if not any(img_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                 img_name += '.jpg'

            file_path = os.path.join(output_folder, f"{HERO_NAME}_{downloaded_count+1}_{img_name}")
            
            with open(file_path, 'wb') as handler:
                handler.write(img_response.content)
            
            downloaded_count += 1
            print(f"[{downloaded_count}/{max_images}] Unduh berhasil: {file_path}")
            
        except requests.exceptions.RequestException as e:
            pass
        except Exception:
            pass
            
        if downloaded_count >= max_images:
            break

    print(f"\n=================================================")
    print(f"✅ SCRAPING SELESAI untuk {HERO_NAME}. Total gambar diunduh: {downloaded_count}")
    print("=================================================")


if __name__ == '__main__':
    scrape_pinterest(SEARCH_TERM, OUTPUT_DIR, MAX_IMAGES)