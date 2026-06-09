import json
import time
import random
import os
import logging
from curl_cffi import requests

# Configuration
DATA_DIR = "navi_mumbai_scraped_data"
LOG_FILE = "navi_mumbai_scraped_data_log.txt"
os.makedirs(DATA_DIR, exist_ok=True)

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)

def get_random_headers():
    # I use Arch btw ;)
    user_agents = [
        "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": "https://www.magicbricks.com/flats-in-mumbai-for-sale-pppfs",
        "Accept": "application/json, text/plain, */*",
    }

def scrape_pages():
    total_pages = 100 # Adjusted to 100 pages as requested
    # magicbricks doesn't allow to scrape beyond page 100
    pages = list(range(1, total_pages + 1))
    random.shuffle(pages)
    
    for page in pages:
        filename = os.path.join(DATA_DIR, f"page_{page}.json")
        
        # 1. Skip already scraped files
        if os.path.exists(filename):
            continue 
            
        remaining = len([p for p in pages if not os.path.exists(os.path.join(DATA_DIR, f"page_{p}.json"))])
        logging.info(f"Scraping Page {page} | Remaining: {remaining} | Progress: {((total_pages - remaining)/total_pages)*100:.2f}%")
        
        params = {'editSearch': 'Y', 'category': 'S', 'city': '4341', 'page': page}
        
        # 2. Fail-safe retry logic (up to 3 times per page)
        retries = 3
        while retries > 0:
            try:
                resp = requests.get(
                    "https://www.magicbricks.com/mbsrp/propertySearch.html",
                    params=params,
                    headers=get_random_headers(),
                    impersonate="firefox",
                    timeout=30
                )
                
                # Check for blocking
                if resp.status_code in [403, 406, 429]:
                    logging.error(f"BLOCKED! Status: {resp.status_code}. Cooling down for 10 mins...")
                    time.sleep(600)
                    retries -= 1
                    continue
                
                if resp.status_code == 200:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(resp.json(), f, indent=4)
                    logging.info(f"SUCCESS: {filename} (Size: {len(resp.text)} chars)")
                    break # Success, move to next page
                
            except Exception as e:
                logging.error(f"Error on page {page}: {e}. Retries left: {retries-1}")
                time.sleep(60)
                retries -= 1
        
        # Human-like delay after every request
        time.sleep(random.uniform(20, 40))

if __name__ == "__main__":
    logging.info("Scraper initiated for 100 pages...")
    scrape_pages()
    logging.info("Scraper finished.")
