from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_reviews(movie_name, max_reviews=20):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')  # Uncomment for headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Go to IMDb and search the movie
        driver.get("https://www.imdb.com")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'suggestion-search'))
        )
        search_box.send_keys(movie_name)
        search_box.send_keys(Keys.RETURN)

        # Step 2: Click the first search result
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c a"))
        )
        driver.find_element(By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c a").click()

        # Step 3: Click the 'User Reviews' tab
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/reviews']"))
        )
        review_tab = driver.find_element(By.CSS_SELECTOR, "a[href*='/reviews']")
        driver.execute_script("arguments[0].click();", review_tab)

        # Step 4: Wait for reviews to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div"))
        )
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div")
        reviews = [el.text.strip() for el in review_elements if el.text.strip()]

        return reviews[:max_reviews]

    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

    finally:
        driver.quit()


