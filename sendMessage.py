import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.remote.webelement import WebElement

WAIT_TIME = 2
HEADLESS = False

def main():

    driver = initialize_driver(2, False)
    driver.get("https://x.com/jakegagain/")
    time.sleep(10)
    button = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/button[2]")
    if(button != None):
        button.click()

    time.sleep(5)

    button = driver.find_element(By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/button").click()
    if(button != None):
        button.click()
    else:
        print("Button not found")

    time.sleep(2)
    print(button)




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