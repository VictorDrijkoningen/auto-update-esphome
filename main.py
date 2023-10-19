import os
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import schedule


def update_esphome_via_selenium(esphometarget, authentication = None):
    print("Starting ESPHOME Update All")
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    # subprocess.Popen("geckodriver")
    # time.sleep(50)
    with webdriver.Firefox(options=opts) as driver:

        driver.maximize_window()
        time.sleep(0.5)

        driver.get('http://'+esphometarget)
        time.sleep(2)

        try:
            if not (authentication is None or authentication == [None, None] ):
                #There is authentication needed
                #driver.save_screenshot("/tmp/screenshots/1.beforeauth.png")
                input_username = driver.find_element(By.ID , "username-field")
                input_username.send_keys(authentication[0])
                input_username = driver.find_element(By.ID , "password-field")
                input_username.send_keys(authentication[1])
                #driver.save_screenshot("/tmp/screenshots/2.aftertyping.png")
                input_submit = driver.find_element(By.ID, "login-form-submit")
                input_submit.click()
                #driver.save_screenshot("/tmp/screenshots/3.afterauth.png")



            #press first update_all button
            button_encasing = driver.find_element(By.XPATH, "//esphome-header-menu").shadow_root
            button_encasing.find_element(By.CSS_SELECTOR, "mwc-button").click()
            #driver.save_screenshot("/tmp/screenshots/4.dialog.png")


            time.sleep(2)

            #press second update_all button in dialog
            dialog = driver.find_element(By.XPATH, "//esphome-confirmation-dialog")
            button_encasing = dialog.shadow_root.find_element(By.CSS_SELECTOR, "mwc-dialog")
            button_encasing.find_element(By.XPATH, "mwc-button[2]").click()
            
            #wait for all esp devices to be updated
            print("waiting for update to finish")

            time.sleep(100) #todo finish when actually finished

            driver.save_screenshot("/tmp/screenshots/999.done.png")
            print("Selenium Job ran successfully")

        except selenium.common.exceptions.NoSuchElementException as e:
            print("Some elements could not be found in esphome", e)
            print("ERROR: ESPHOME UPDATING FAILED")

        


def update_esphome_via_socket(esphometarget):
    '''Update esphome devices via a socket call'''
    pass


def job():
    '''check datetime and start job with right mode'''
    if datetime.date.today().day not in [15]:
        print("Not today m'dude", datetime.date.today().day)
        return

    if os.environ['MODE'] == 'selenium':
        update_esphome_via_selenium(os.environ['ESPHOME_TARGET'], [os.environ.get('USERNAME'), os.environ.get('PASSWORD')])
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

    


if __name__ == "__main__":

    #check environment variables
    check_env()

    update_esphome_via_selenium(os.environ['ESPHOME_TARGET'], [os.environ.get('USERNAME'), os.environ.get('PASSWORD')])

    schedule.every().day.at("19:00").do(job)
    print("Schedule Started")
    while True:
        schedule.run_pending()
        time.sleep(1)
