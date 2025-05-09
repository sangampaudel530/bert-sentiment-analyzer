import os
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "your_api_key_here")  # Make sure to set this in Render's environment variables

def get_movie_id(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Log the response to debug
    logger.info(f"OMDB API response for {title}: {data}")

    if data.get("Response") == "True":
        return data.get("imdbID")
    else:
        logger.warning(f"Movie not found: {title} - Response: {data.get('Error')}")
    return None

def get_reviews(movie_id, max_reviews=20):
    reviews = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = f"https://www.imdb.com/title/{movie_id}/reviews"
        logger.info(f"Opening: {url}")
        driver.get(url)

        # Wait for the reviews to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ipc-overflowText--listCard"))
        )

        try:
            # Close any login or popup if exists
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(1)
        except Exception:
            pass

        # Scroll to load more reviews
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div")
        logger.info(f"Found {len(review_blocks)} reviews.")

        for block in review_blocks[:max_reviews]:
            reviews.append(block.text.strip())

    except Exception as e:
        logger.error(f"Error: {str(e)}")

    finally:
        driver.quit()

    return reviews