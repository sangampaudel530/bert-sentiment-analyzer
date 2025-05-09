import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

OMDB_API_KEY = "ad0e3181"  # Replace with your actual OMDb key

def get_movie_id(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("imdbID")
    return None

def get_reviews(movie_id, max_reviews=20):
    reviews = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        url = f"https://www.imdb.com/title/{movie_id}/reviews"
        print(f"Opening: {url}")
        driver.get(url)
        time.sleep(3)

        # Close login popup if it appears
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            time.sleep(1)
        except:
            pass

        # Scroll down to load more reviews
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Correct review selector (IMDb May 2025)
        review_blocks = driver.find_elements(
            By.CSS_SELECTOR,
            "div.ipc-overflowText--listCard div > div > div"
        )

        print(f"Found {len(review_blocks)} reviews.")
        for block in review_blocks[:max_reviews]:
            reviews.append(block.text.strip())

    except Exception as e:
        print("Error:", str(e))

    finally:
        driver.quit()

    return reviews
