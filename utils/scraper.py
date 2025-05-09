import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

OMDB_API_KEY = "ad0e3181"  # Replace with your own key if needed

def get_movie_id(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("imdbID")
    return None

def get_reviews(movie_id, max_reviews=20):
    reviews = []

    # Set Chrome options for headless browser in Railway
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # Set Chromium and chromedriver path for Railway
    chrome_bin = os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    driver_bin = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
    chrome_options.binary_location = chrome_bin

    driver = webdriver.Chrome(executable_path=driver_bin, options=chrome_options)

    try:
        url = f"https://www.imdb.com/title/{movie_id}/reviews"
        driver.get(url)
        time.sleep(3)

        # Close popup if present
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(1)
        except:
            pass

        # Scroll down to load more reviews
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div")

        for block in review_blocks[:max_reviews]:
            reviews.append(block.text.strip())

    except Exception as e:
        print(f"[ERROR] Failed to fetch reviews: {e}")

    finally:
        driver.quit()

    return reviews
