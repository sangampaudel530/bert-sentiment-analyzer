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
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36')

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
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c a"))
        )
        driver.find_element(By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c a").click()

        time.sleep(2)  # Give the movie page time to load

        # Step 3: Navigate to the 'User reviews' tab
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.sc-466f296a-0.jLmGLJ li:nth-child(2) a"))
        )
        user_review_link = driver.find_element(By.CSS_SELECTOR, "div.sc-466f296a-0.jLmGLJ li:nth-child(2) a")
        driver.execute_script("arguments[0].click();", user_review_link)

        # Step 4: Scroll down to trigger lazy load
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Step 5: Wait for the reviews to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div"))
        )

        # Step 6: Collect reviews
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.ipc-overflowText--listCard div > div > div")
        reviews = [el.text.strip() for el in review_elements if el.text.strip()]

        return reviews[:max_reviews]

    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

    finally:
        driver.quit()

# Optional: run standalone for testing
if __name__ == "__main__":
    movie = "Interstellar"
    reviews = get_reviews(movie, max_reviews=10)
    if reviews:
        print(f"\nReviews for {movie}:\n")
        for i, r in enumerate(reviews, 1):
            print(f"{i}. {r}\n")
    else:
        print("No reviews found.")
