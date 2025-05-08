# utils/scraper.py

import time
import requests
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

OMDB_API_KEY = "ad0e3181"  # Replace this with your actual OMDB API key


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
    chrome_options.add_argument("--headless")  # keep headless for deployment
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # Try to set binary location for Linux servers (e.g., Streamlit Cloud)
    if shutil.which("chromium-browser"):
        chrome_options.binary_location = shutil.which("chromium-browser")
    elif shutil.which("google-chrome"):
        chrome_options.binary_location = shutil.which("google-chrome")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        url = f"https://www.imdb.com/title/{movie_id}/reviews"
        print(f"Opening: {url}")
        driver.get(url)
        time.sleep(3)

        # Close login popup if exists
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(1)
        except:
            pass

        # Scroll to load more
        scroll_pause_time = 2
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        # New review selector based on updated IMDB layout
        review_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            "div.ipc-overflowText--listCard div > div > div"
        )

        print(f"Found {len(review_blocks)} reviews.")
        for block in review_blocks[:max_reviews]:
            reviews.append(block.text.strip())

    except Exception as e:
        print("Error fetching reviews:", str(e))

    finally:
        driver.quit()

    return reviews
