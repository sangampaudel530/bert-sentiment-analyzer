from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def _init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def get_movie_id(movie_name):
    search_name = movie_name.replace(" ", "+")
    search_url = f"https://www.imdb.com/find?q={search_name}&s=tt&ttype=ft&ref_=fn_ft"

    driver = _init_driver()
    driver.get(search_url)
    time.sleep(2)

    try:
        first_result = driver.find_element(By.CSS_SELECTOR, "td.result_text a")
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

    driver = _init_driver()
    driver.get(url)
    time.sleep(3)

    reviews = []

    try:
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.review-container")
        for review_element in review_elements[:max_reviews]:
            try:
                text = review_element.find_element(By.CSS_SELECTOR, ".text.show-more__control").text
                reviews.append(text)
            except:
                continue
    except Exception as e:
        print("Error extracting reviews:", e)
    finally:
        driver.quit()

    return reviews
