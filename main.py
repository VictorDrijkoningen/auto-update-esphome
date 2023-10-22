import os
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import schedule


def save_screenshot(driver, tag):
    '''if the development env var is set, then store the screenshot'''
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        driver.save_screenshot(f"/tmp/screenshots/{datetime.date.today()}-{tag}.png")


def update_esphome_via_selenium(esphometarget, authentication = None):
    '''update esphome devices via a selenium operated firefox instance'''

    print("Starting ESPHOME Update All")
    opts = FirefoxOptions()
    opts.add_argument("--headless")

    with webdriver.Firefox(options=opts) as driver:

        driver.maximize_window()
        driver.get('http://'+esphometarget)
        time.sleep(2)

        try:
            if not (authentication is None or authentication == [None, None] ):
                #There is authentication needed
                save_screenshot(driver, "1.beforeauth")
                input_username = driver.find_element(By.ID , "username-field")
                input_username.send_keys(authentication[0])
                input_username = driver.find_element(By.ID , "password-field")
                input_username.send_keys(authentication[1])
                save_screenshot(driver, "2.aftertyping")
                input_submit = driver.find_element(By.ID, "login-form-submit")
                input_submit.click()
                save_screenshot(driver, "3.afterauth")



            #press first update_all button
            button_encasing = driver.find_element(By.XPATH, "//esphome-header-menu").shadow_root
            button_encasing.find_element(By.CSS_SELECTOR, "mwc-button").click()
            save_screenshot(driver, "4.dialog")


            time.sleep(2)

            #press second update_all button in dialog
            dialog = driver.find_element(By.XPATH, "//esphome-confirmation-dialog").shadow_root
            button_encasing = dialog.find_element(By.CSS_SELECTOR, "mwc-dialog")
            button_encasing.find_element(By.XPATH, "mwc-button[2]").click()

            #wait for all esp devices to be updated
            print("waiting for update to finish")

            #wait for summary to appear or timeout this action
            starttime = time.time()
            while True:
                time.sleep(1)
                if time.time() - starttime > 1000:
                    print("ERROR: Failed to find update dialog, update failed!")
                    save_screenshot(driver, "5.failed")
                    break
                try:
                    step1 = driver.find_element(By.CSS_SELECTOR, "esphome-update-all-dialog")
                    step1.shadow_root.find_element(By.CSS_SELECTOR, "esphome-process-dialog")

                    save_screenshot(driver, "5.done")
                    print(f"Selenium Job successfully pressed update and took {time.time()-starttime}")
                    time.sleep(1)
                    break

                except selenium.common.exceptions.NoSuchElementException:
                    pass #expected because updating takes time.


        except selenium.common.exceptions.NoSuchElementException as e:
            print("Some elements could not be found in esphome", e)
            print("ERROR: ESPHOME UPDATING FAILED")



def update_esphome_via_socket(esphometarget):
    '''Update esphome devices via a socket call'''
    print(f"TODO socket call to {esphometarget}")


def job():
    '''check datetime and start job with right mode'''
    if datetime.date.today().day not in [15]:
        print("Not today m'dude", datetime.date.today().day)
        return

    if os.environ['MODE'] == 'selenium':
        auth = [os.environ.get('USERNAME'), os.environ.get('PASSWORD')]
        update_esphome_via_selenium(os.environ['ESPHOME_TARGET'], auth)
    elif os.environ['MODE'] == 'socket':
        update_esphome_via_socket(os.environ['ESPHOME_TARGET'])
    else:
        print("How did we get here?")
        exit(1)



def check_env():
    '''function checks the environment variables to be suitable for this code'''

    ip_regex = r'[0-9]+(?:\.[0-9]+){3}:[0-9]+' #TODO include ipv6, but good enough for now.

    if os.environ.get('MODE') != 'selenium' and os.environ.get('MODE') != 'socket':
        print(f"ERROR: unknown mode {os.environ.get('MODE')}")
        exit(1)

    if not re.search(ip_regex, str(os.environ.get('ESPHOME_TARGET'))):
        print("ERROR: esphome target not valid")
        exit(1)

    if not os.environ.get('PASSWORD') is None:
        if os.environ.get('USERNAME') is None:
            print("ERROR: USERNAME EMPTY")
            exit(1)
    if not os.environ.get('USERNAME') is None:
        if os.environ.get('PASSWORD') is None:
            print("ERROR: PASSWORD EMPTY")
            exit(1)

    if os.environ.get('USERNAME') is None and os.environ.get('PASSWORD') is None:
        print("No credentials found, assuming no credentials needed")
    else:
        print("Credentials found, rolling with credentials")

    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        print("Logging screenshots")
    else:
        print("Not logging screenshots")


if __name__ == "__main__":
    with open('VERSION', encoding="utf-8") as file:
        print(file.read())

    #check environment variables
    check_env()

    schedule.every().day.at("01:00").do(job)
    print("Schedule Started")
    while True:
        schedule.run_pending()
        time.sleep(1)
