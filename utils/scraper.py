from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_reviews(movie_name, max_reviews=20):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Optional: Run headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: IMDb search
        driver.get("https://www.imdb.com")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'suggestion-search'))
        )
        search_box.send_keys(movie_name)
        search_box.send_keys(Keys.RETURN)

        # Step 2: Click the first result
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c a"))
        )
        driver.find_element(By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c a").click()

        time.sleep(2)  # Give page time to fully load

        # Step 3: Click the 'User Reviews' tab using verified selector
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.sc-466f296a-0.jLmGLJ li:nth-child(2) a"))
        )
        user_review_link = driver.find_element(By.CSS_SELECTOR, "div.sc-466f296a-0.jLmGLJ li:nth-child(2) a")
        driver.execute_script("arguments[0].click();", user_review_link)

        # Step 4: Wait for review content to load
        reviews = []
        while len(reviews) < max_reviews:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ipc-overflowText--listCard div.ipc-html-content"))
            )
            review_elements = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div.ipc-html-content")
            new_reviews = [el.text.strip() for el in review_elements if el.text.strip()]
            reviews.extend(new_reviews)

            # If we have reached or exceeded the max_reviews, break the loop
            if len(reviews) >= max_reviews:
                reviews = reviews[:max_reviews]  # Limit the list to max_reviews
                break

            # Step 5: Check if there's a next page of reviews
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.load-more--next-page"))
                )
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(2)  # Wait for the next page to load
            except Exception as e:
                print("No more reviews or failed to load next page.")
                break

        return reviews

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        driver.quit()
