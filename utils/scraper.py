from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_movie_id(movie_name):
    search_name = movie_name.replace(" ", "+")
    search_url = f"https://www.imdb.com/find?q={search_name}&s=tt&ttype=ft&ref_=fn_ft"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(search_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.ipc-metadata-list-summary-item__t"))
        )
        first_result = driver.find_element(By.CSS_SELECTOR, "a.ipc-metadata-list-summary-item__t")
        href = first_result.get_attribute("href")
        movie_id = href.split("/")[4]
        return movie_id
    except Exception as e:
        print("Movie not found:", e)
        return None
    finally:
        driver.quit()


def get_reviews(movie_id, max_reviews=20):
    url = f"https://www.imdb.com/title/{movie_id}/reviews"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)
    reviews = []

    try:
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.review-container")
        for review_element in review_elements[:max_reviews]:
            review_text = review_element.find_element(By.CSS_SELECTOR, ".text.show-more__control").text
            reviews.append(review_text)
    except Exception as e:
        print("Error extracting reviews:", e)
    finally:
        driver.quit()

    return reviews
