import json
import os
import sys
import time
from datetime import datetime, timezone
import csv
from thefuzz import fuzz

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

LINK = "https://www.usphonebook.com/address/3901-winfield-ave_fort-worth-tx"

WAIT_TIME = 2
HEADLESS_MODE = False


def main():
    results = load_users()

    driver = initialize_driver(WAIT_TIME, HEADLESS_MODE)

    for result in results:
        scrape_location(result, driver)


def scrape_location(result, driver: WebDriver):
    street = result["address"]["streetAddress"].lower().replace(" ", "-")
    state = result["address"]["stateCode"].lower()
    city = result["address"]["cityName"].lower().replace(" ", "-")
    url = f"https://www.usphonebook.com/address/{street}_{city}-{state}"

    driver.get(url)

    residents = driver.find_elements(By.CSS_SELECTOR, ".ls_number-text a")
    ratio = 0
    owner_link = ""
    owner_name = f"{result["owner1FirstName"]} {result["owner1LastName"]}"

    for resident in residents:
        name = resident.get_attribute("innerText")
        if fuzz.partial_ratio(owner_name, name) > ratio:
            ratio = fuzz.partial_ratio(owner_name, name)
            owner_link = resident.get_attribute("href")
    
    if owner_link == "":
        return

    print(f"Link: {owner_link}")
    driver.get(owner_link)

    try:
        owner_name = driver.find_element(By.CLASS_NAME, "header-name").get_attribute("innerText")
    except:
        return
    try:
        owner_age = driver.find_element(By.CSS_SELECTOR, "h3 span:nth-child(2)").get_attribute("innerText").strip().removesuffix("years old").strip()
    except:
        owner_age = ""
    try:
        owner_phone = driver.find_element(By.CSS_SELECTOR, '[itemprop="telephone"]').get_attribute("innerText").strip()
    except:
        owner_phone = ""
    try:
        owner_email = driver.find_element(By.CSS_SELECTOR, '[href^="mailto"]').get_attribute("innerText").strip()
    except:
        owner_email = ""

    data = {
        "NAME": owner_name,
        "NUMBER": owner_phone,
        "AGE": owner_age,
        "STATE": result["address"]["stateCode"],
        "CITY": result["address"]["cityName"],
        "ADDRESS": result["address"]["streetAddress"],
        "ZIP": result["address"]["zip"],
        "EMAIL": owner_email
    }

    with open(f"Fort-Worth/mls.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect="excel")
        writer.writerow(list(data.values()))


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


def open_in_new_window(driver: WebDriver, item_url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(item_url)
    driver.implicitly_wait(0.2)


def load_users():
    with open("results.json") as f:
        s = f.read()

    return json.loads(s)

def create_output():
    with open(f"Fort-Worth/mls.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect="excel")
        writer.writerow(["NAME","NUMBER","AGE","STATE","CITY","ADDRESS","ZIP","EMAIL"])


if __name__ == "__main__":
    main()
