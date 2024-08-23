import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.remote.webelement import WebElement

WAIT_TIME = 2
HEADLESS = False

def main():

    driver = initialize_driver(2, False)
    scrape_following_list("jakegagain", driver)
    
    driver.quit()
    

def scrape_following_list(account, driver: WebDriver):
    url = f"https://x.com/{account.strip('@')}/following"
    driver.get(url)

    time.sleep(10)

    following_accounts = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    try:
        button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/button')
        if(button):
            button.click()
    except:
        print("Working Correctly")

    time.sleep(3)
    while True:
        
        # for i in range(0, len(userdivs)):
            # print(driver.find_element(By.XPATH, f'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[{i}]/div/section/div/div/div[2]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]'))
        # //*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]
        # print(len(userdivs))
        # print(userdivs[0].find_element(By.XPATH, '//div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]').text)
        userdivs = driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div')

        for div in userdivs:
            try:
                # Use relative XPath to find elements within the current div
                username = div.find_element(By.XPATH, './/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]').text
                handle = div.find_element(By.XPATH, './/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span').text

                value = [username, handle]

                if value not in following_accounts:
                    following_accounts.append(value)

            except Exception as e:
                print(f"An error occurred: {e}")
        # usernamediv = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] div[dir="ltr"] span')
        # print(userdivs[1].find_element(By.XPATH, '//div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]').text)
        # print(userdivs[1].find_element(By.XPATH, '//div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span').text)
        
        # print(following_accounts)
        
        
        # username = driver.find_elements(By.XPATH, '//div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]')
        # for name in usernamediv:
        #     account_name = name.text
        #     if account_name not in following_accounts and account_name != "Follow":
        #         following_accounts.append(account_name)
        # handle = driver.find_elements(By.XPATH, '//div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span')
        # print(username[0].text, handle[0].text)           

        # Scroll down by smaller increments
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Wait for the new accounts to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    save_following_data(account, following_accounts)


def save_following_data(account, following_accounts):
    with open(f"users.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect="excel")
        for following in following_accounts:
            writer.writerow([account, following[0], following[1]])


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



if __name__ == "__main__":
    main()