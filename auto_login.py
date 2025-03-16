# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0026ABF74B390E5D859C52A386CAD577933CAACA2AF21969CF7C519CDD0BE4A174E65FF06B7D7C3A9953809852BEE977534626914533B80C6C8477D9D497E126D83884B847A33DC0290456824824E4859EDBF7614EF65EBEC4F3F80D72C84623DCEBDA4D9007E5EFD0ADA9FDF68AFF6771F98CEAC0EA12BCCC5EAAA82367BB9CBCDCF0500DC48DCF9701517E4861D7DA1B5E324D56DDE14ABF53F09877394357094FD14F8149BAF1460E78514C78CF8CB42020F4E42204806251E8CEE7B1C495C22EDB1E73D8CA92A214287B0D02F424B4819BBB31E6AF3C1356F3619D90EB23F0A164D381FFA77622DBF0A761184357E6F05EA0013A69E4A9E532BBAA272E4150003EB41E9D73F153DFE1873971FA65D3A5CBD5793A381C683B24AB73CCD783416B0F3C2F49A7D7D98B6B38E2D0C687914F152124AAFE2D70A99C65D32E835E42"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
