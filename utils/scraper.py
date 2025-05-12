from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_reviews(movie_name):
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ipc-overflowText--listCard div.ipc-html-content"))
        )
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div.ipc-html-content")
        reviews = [el.text.strip() for el in review_elements if el.text.strip()]

        return reviews

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    movie = "Interstellar"
    reviews = get_reviews(movie)
    if reviews:
        print(f"Reviews for {movie}:\n")
        for idx, review in enumerate(reviews, 1):
            print(f"{idx}. {review}\n")
    else:
        print("No reviews found.")
