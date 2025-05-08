import time
import requests
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
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # Set the location of Chrome in deployment
    chrome_path = shutil.which("chromium-browser") or shutil.which("google-chrome")
    if chrome_path:
        chrome_options.binary_location = chrome_path

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
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

        review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div")

        print(f"Found {len(review_blocks)} reviews.")
        for block in review_blocks[:max_reviews]:
            reviews.append(block.text.strip())

    except Exception as e:
        print("Error:", str(e))

    finally:
        driver.quit()

    return reviews
