# utils/scraper.py

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

OMDB_API_KEY = "ad0e3181"

# Use these paths on Render
RENDER_CHROME_BINARY = "/usr/bin/chromium-browser"
RENDER_CHROMEDRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"

def get_movie_id(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("imdbID"), data.get("Poster")
    return None, None

def get_reviews(movie_id, max_reviews=20):
    reviews = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # Check if we're on Render
    if os.path.exists(RENDER_CHROMEDRIVER_PATH):
        chrome_options.binary_location = RENDER_CHROME_BINARY
        service = Service(RENDER_CHROMEDRIVER_PATH)
    else:
        # For local development
        service = Service(ChromeDriverManager().install())

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        url = f"https://www.imdb.com/title/{movie_id}/reviews"
        print(f"Opening: {url}")
        driver.get(url)
        time.sleep(3)

        try:
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(1)
        except:
            pass

        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        review_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            "div.ipc-overflowText--listCard div > div > div"
        )

        for block in review_blocks[:max_reviews]:
            text = block.text.strip()
            if text:
                reviews.append(text)

    except Exception as e:
        print("Error while scraping reviews:", str(e))

    finally:
        driver.quit()

    return reviews
