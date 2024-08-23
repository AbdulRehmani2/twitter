import json
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

WAIT_TIME = 2
HEADLESS_MODE = False
TWITTER_USERNAME = "Ghazi2238"
TWITTER_PASSWORD = ""


def main():
    # accounts_to_scrape = load_users()
    driver = initialize_driver(WAIT_TIME, HEADLESS_MODE)

    file_path = 'jakegagain_following.csv'
    handles_list = extract_handles_from_csv(file_path)
    
    handles = extract_handles_from_csv("following_copy.csv")

    names = []

    for i in handles:
        if(i[0] == ("@")):
            names.append(i)
    
    names = [item for item in names if item not in handles_list]
    
    names = names[1 : 60]
    
    names = set(names)
    
    for name in names:
        scrape_following_list(name, driver)
    
    
    
    
    # for account in names:
    #     # get_twitter_followers(handles_list[1], driver)
        # scrape_following_list(account, driver)
        
    

    # for account in accounts_to_scrape:
        # scrape_following_list(account, driver)
        # driver.get("https://twitter.com/jakegagain/following")
        # print(account)

    # driver.quit()
    
def get_twitter_followers(username, driver: WebDriver):

    try:
        # Navigate to the Twitter user's page
        twitter_url = f"https://twitter.com/{username.strip('@')}"
        driver.get(twitter_url)

        # Wait for the page to load (adjust time.sleep as needed)
        time.sleep(5)

        # Locate the followers count element
        follower_count_element = driver.find_element(By.XPATH, f"//a[contains(@href, '/{username}/verified followers')]/span[1]")

        # Extract and return the follower count
        followers_count = follower_count_element.get_attribute("title")
        print(followers_count)
        return followers_count

    except Exception as e:
        print(f"Error fetching followers for {username.strip('@')}: {e}")
        return None
    
    

def extract_handles_from_csv(file_path):
    handles = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                handles.append(row[1].strip())
    return handles

# Example usage:


def scrape_following_list(account, driver: WebDriver):
    url = f"https://twitter.com/{account.strip('@')}/following"
    driver.get(url)

    time.sleep(10)  # Wait for the page to load

    following_accounts = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        usernamediv = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] div[dir="ltr"] span')
        for name in usernamediv:
            account_name = name.text
            if account_name not in following_accounts and account_name != "Follow":
                following_accounts.append(account_name)
            

        # Scroll down by smaller increments
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Wait for the new accounts to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    save_following_data(account, following_accounts)


def save_following_data(account, following_accounts):
    with open(f"following.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect="excel")
        for following in following_accounts:
            writer.writerow([account, following])
            
def save_follower_data(account, followers):
    with open(f"followers.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect="excel")
        writer.writerow(["Account, Followers"])
        writer.writerow([account, followers])



def initialize_driver(wait, headless):
    options = Options()
    service = Service(ChromeDriverManager().install())

    if headless:
        options.add_argument("--headless")

    options.add_argument(
        "user-data-dir=C:\\Users\\AbdulRehman\\AppData\\Local\\Google\\Chrome\\User Data"
    )
    options.add_argument("profile-directory=Default")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--lang=en-US")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(wait)
    return driver


# def load_users():
#     with open("results.json") as f:
#         s = f.read()
#     return json.loads(s)


if __name__ == "__main__":
    main()
