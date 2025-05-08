import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

OMDB_API_KEY = "ad0e3181"  # Replace with your valid OMDb key

# Paths for Render deployment
CHROME_BINARY_PATH = "/usr/bin/chromium-browser"
CHROMEDRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"

def get_movie_id(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "True":
            return data.get("imdbID"), data.get("Poster")
    except Exception as e:
        print("Error fetching movie ID:", e)
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

    driver = None
    try:
        # If deploying on Render, use system Chrome and chromedriver
        if os.path.exists(CHROMEDRIVER_PATH) and os.path.exists(CHROME_BINARY_PATH):
            chrome_options.binary_location = CHROME_BINARY_PATH
            service = Service(CHROMEDRIVER_PATH)
        else:
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=chrome_options)
        url = f"https://www.imdb.com/title/{movie_id}/reviews"
        print(f"Opening: {url}")
        driver.get(url)
        time.sleep(3)

        # Try to close login popup if it appears
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(1)
        except:
            pass

        # Scroll multiple times to load more reviews
        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Primary selector (new IMDb layout)
        review_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            "div.review-container div.content div.text.show-more__control"
        )

        # Fallback selector if primary fails
        if not review_blocks:
            review_blocks = driver.find_elements(
                By.CSS_SELECTOR,
                ".text.show-more__control"
            )

        print(f"Found {len(review_blocks)} reviews.")
        for block in review_blocks[:max_reviews]:
            text = block.text.strip()
            if text:
                reviews.append(text)

    except Exception as e:
        print("Error while scraping reviews:", str(e))

    finally:
        if driver:
            driver.quit()

    return reviews
