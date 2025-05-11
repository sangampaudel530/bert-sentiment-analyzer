from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_reviews(movie_id, max_reviews=20):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    # Set up Chrome driver service
    service = Service("/usr/bin/chromedriver")

    # Start driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # IMDb review page
    url = f"https://www.imdb.com/title/{movie_id}/reviews"
    driver.get(url)

    # Scroll and click "Load More" until enough reviews
    while True:
        try:
            load_more = driver.find_element("xpath", '//button[contains(text(), "Load More")]')
            if load_more:
                driver.execute_script("arguments[0].click();", load_more)
                time.sleep(2)
        except:
            break

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        reviews = soup.select("div.review-container")
        if len(reviews) >= max_reviews:
            break

    # Final review extraction
    reviews = soup.select("div.review-container")
    extracted = []
    for r in reviews[:max_reviews]:
        review_text = r.select_one("div.text.show-more__control")
        if review_text:
            extracted.append(review_text.text.strip())

    driver.quit()
    return extracted
