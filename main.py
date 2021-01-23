from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

driver = None

# get login creds from creds.json
def getCreds():
    data = None
    with open("creds.json") as json_file:
        data = json.load(json_file)
        return data["email"], data["password"]


def start_browser_and_login():

    global driver

    # settings for browser
    opt = Options()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--start-maximized")
    # Pass the argument 1 to allow and 2 to block
    opt.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
        },
    )

    # start browser
    driver = webdriver.Chrome(chrome_options=opt, service_log_path="NUL")
    driver.get("https://teams.microsoft.com")

    # wait for page
    WebDriverWait(driver, 10000).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

    # check if login is required
    if "login.microsoftonline.com" in driver.current_url:
        login()

    # wait for login
    while not "teams.microsoft.com/_#/" in driver.current_url:
        pass
    time.sleep(2)


def login():
    global driver

    # get creds for login
    email, password = getCreds()

    # login required
    emailField = driver.find_element_by_xpath('//*[@id="i0116"]')
    emailField.click()
    emailField.send_keys(email + Keys.ENTER)
    # driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()  # Next button
    time.sleep(2)
    passwordField = driver.find_element_by_xpath('//*[@id="i0118"]')
    passwordField.click()
    passwordField.send_keys(password + Keys.ENTER)
    # driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()  # Sign in button
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()  # remember login
    except:
        pass
    time.sleep(2)


def go_to_assigments():
    global driver

    # navigate to assigment
    driver.find_element_by_xpath(
        '//*[@id="app-bar-66aeee93-507d-479a-a3ef-8f494af43945"]'
    ).click()

    time.sleep(7)


def get_list_of_assigments():
    global driver

    elements = []

    while elements == []:
        elements = driver.find_elements_by_class_name("assignment-card__1ClA-")
        print(".")

    print(elements)


if __name__ == "__main__":

    start_browser_and_login()
    go_to_assigments()
    get_list_of_assigments()
