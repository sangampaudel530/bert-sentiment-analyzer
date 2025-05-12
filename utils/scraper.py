from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_reviews(movie_name, max_reviews=20):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # Use modern headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Go to IMDb and search for the movie
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

        time.sleep(2)  # Give the movie page time to load

        # Step 3: Navigate to the 'User reviews' tab
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.sc-466f296a-0.jLmGLJ li:nth-child(2) a"))
        )
        user_review_link = driver.find_element(By.CSS_SELECTOR, "div.sc-466f296a-0.jLmGLJ li:nth-child(2) a")
        driver.execute_script("arguments[0].click();", user_review_link)

        # Step 4: Wait for the reviews to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ipc-overflowText--listCard div.ipc-html-content"))
        )

        # Step 5: Collect reviews
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div.ipc-html-content")
        reviews = [el.text.strip() for el in review_elements if el.text.strip()]

        return reviews[:max_reviews]

    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

    finally:
        driver.quit()
