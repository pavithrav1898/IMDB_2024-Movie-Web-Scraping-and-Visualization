from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import re
import random
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-gpu')
options.add_argument('--mute-audio')
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

def web_scrap():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        release_date = "2024-01-01,2024-12-31"
        genres = ['thriller', 'documentary','drama','comedy','horror']

        for genre in genres:
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={release_date}&genres={genre}"
            driver.get(url)
            time.sleep(random.uniform(2, 4))

            with open(f"{genre}.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["movie_name", "genre", "rating", "vote_count", "duration"])

                scraped_count = 0
                while True:
                    movie_containers = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
                    current_count = len(movie_containers)
                    print(f"Movies loaded so far: {current_count}")
                    if not movie_containers:
                        print(f"No movies found for genre {genre}")
                        break

                    for movie in movie_containers[scraped_count:]:
                        try:
                            movie_name = movie.find_element(By.CSS_SELECTOR, "a h3").text
                            movie_name = re.sub(r"\d+\.", " ", movie_name).strip()
                        except NoSuchElementException:
                            movie_name = "N/A"

                        try:
                            rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
                        except NoSuchElementException:
                            rating = "N/A"

                        try:
                            vote_element = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text
                            vote_count = re.sub(r"[()\u00A0]", "", vote_element).strip()
                            if "K" in vote_count.upper():
                                vote_count = int(float(vote_count.upper().replace("K", "")) * 1000)
                            else:
                                vote_count = int(vote_count.replace(",", ""))
                        except (NoSuchElementException, ValueError):
                            vote_count = "N/A"

                        try:
                            hours = movie.find_element(By.CSS_SELECTOR, "div.sc-15ac7568-6.fqJJPW.dli-title-metadata")
                            spans = hours.find_elements(By.TAG_NAME, "span")
                            duration = spans[1].text if len(spans) > 1 else "N/A"
                        except NoSuchElementException:
                            duration = "N/A"

                        writer.writerow([movie_name, genre, rating, vote_count, duration])
                        print(f"{movie_name}, {genre}, {rating}, {vote_count}, {duration}")

                    scraped_count = current_count

                    # Check if we need to click
                    try:
                        load_more_btn = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ipc-see-more__button"))
                        )
                        driver.execute_script("arguments[0].click();", load_more_btn)
                        print(f"Clicked '50 more' button after {current_count} movies...")
                        time.sleep(random.uniform(2, 4))
                    except TimeoutException:
                        print("No click needed this round, continuing...")
                        time.sleep(random.uniform(2, 4))
                        break

        driver.quit()
        print("\n Scraping finished! Data saved in csv files")

    except Exception as e:
        print(f"An error occurred: {e}")
