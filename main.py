import os
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import schedule

LOGFILE = "./app.log"

def save_screenshot(driver, tag):
    '''if the development env var is set, then store the screenshot'''
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        driver.save_screenshot(f"/tmp/screenshots/{datetime.date.today()}-{tag}.png")


def log(message: str, message2="", timestamp=True) -> None:
    '''global logging function'''
    if timestamp:
        d = datetime.date.today()
        inp = f'{d} - {message} {message2}.'
        print(inp)
    else:
        inp = f'{message} {message2}.'
        print(inp)
    with open(LOGFILE, "a", encoding="utf-8") as logf:
        logf.write(inp+"\n")


def update_esphome_via_selenium(esphometarget, authentication = None):
    '''update esphome devices via a selenium operated firefox instance'''

    log("Starting ESPHOME Update All")
    opts = FirefoxOptions()
    opts.add_argument("--headless")

    with webdriver.Firefox(options=opts) as driver:

        driver.maximize_window()
        driver.get('http://'+esphometarget)
        time.sleep(5)

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


            #check if devices are up-to-date
            devices_list = driver.find_element(By.XPATH, "//esphome-devices-list").shadow_root
            devices = devices_list.find_elements(By.CSS_SELECTOR, "esphome-configured-device-card")
            found_updateable = False
            updateable_devices = 0
            for device in devices:
                card = device.shadow_root.find_element(By.CSS_SELECTOR, 'esphome-card')
                status = card.get_attribute('style')

                if 'update' in status:
                    found_updateable = True
                    updateable_devices += 1

            if not found_updateable:
                log("no updates found in devices, done updating")
                return 1

            log(f"Found {updateable_devices} devices that can be updated")


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
            log("waiting for update to finish")

            #wait for summary to appear or timeout this action
            starttime = time.time()
            oldpage = driver.get_screenshot_as_base64()
            while True:
                time.sleep(3)
                if time.time() - starttime > 1000:
                    log("ERROR: Failed to find update dialog, update failed!")
                    save_screenshot(driver, "5.failed")
                    break

                #compare page to see if nothing is changing anymore
                newpage = driver.get_screenshot_as_base64()
                if newpage == oldpage:
                    log("end of update detected")
                    save_screenshot(driver, "5.success")
                    break
                oldpage = newpage

        except selenium.common.exceptions.NoSuchElementException as e:
            log("Some elements could not be found in esphome", e)
            log("ERROR: ESPHOME UPDATING FAILED")
        return 0


def update_esphome_via_socket(esphometarget, auth):
    '''Update esphome devices via a socket call'''
    log(f"TODO socket call to {esphometarget}")
    exit(1)


def start_update():
    '''start the update process'''
    auth = [os.environ.get('USERNAME'), os.environ.get('PASSWORD')]
    if os.environ['MODE'] == 'selenium':
        update_esphome_via_selenium(os.environ['ESPHOME_TARGET'], auth)
    elif os.environ['MODE'] == 'socket':
        update_esphome_via_socket(os.environ['ESPHOME_TARGET'], auth)



def check_date():
    '''check datetime and start update'''
    run_days = os.environ.get('RUN_DAYS')
    run_days = run_days.replace(' ', '').split(',')
    run_days = [int(i) for i in run_days]

    run_months = os.environ.get('RUN_MONTHS')
    run_months = run_months.replace(' ', '').split(',')
    run_months = [int(i) for i in run_months]

    if datetime.date.today().month not in run_months:
        return

    if datetime.date.today().day not in run_days:
        return

    start_update()

def check_env():
    '''function checks the environment variables to be suitable for this code'''

    ip_regex = r'[0-9]+(?:\.[0-9]+){3}:[0-9]+' #should not exclude ipv6, but good enough for now.

    #check MODE
    if os.environ.get('MODE') != 'selenium' and os.environ.get('MODE') != 'socket':
        log(f"ERROR: unknown mode {os.environ.get('MODE')}")
        exit(1)

    #check IP esphome
    if not re.search(ip_regex, str(os.environ.get('ESPHOME_TARGET'))):
        log("ERROR: esphome target not valid")
        exit(1)

    #check auth
    if not os.environ.get('PASSWORD') is None:
        if os.environ.get('USERNAME') is None:
            log("ERROR: USERNAME EMPTY")
            exit(1)
    if not os.environ.get('USERNAME') is None:
        if os.environ.get('PASSWORD') is None:
            log("ERROR: PASSWORD EMPTY")
            exit(1)

    if os.environ.get('USERNAME') is None and os.environ.get('PASSWORD') is None:
        log("No credentials found, assuming no credentials needed")
    else:
        log("Credentials found, rolling with credentials")

    #check logging
    if os.environ.get("SCREENSHOT_LOG") == "TRUE":
        log("Logging screenshots")

    #check RUN_MONTHS
    if os.environ.get('RUN_MONTHS') is None:
        log("No months to run found, setting to all months")
        os.environ.setdefault('RUN_MONTHS', '1,2,3,4,5,6,7,8,9,10,11,12')

    run_months = os.environ.get('RUN_MONTHS')
    run_months = run_months.replace(' ', '').split(',')
    if len(run_months) == 0:
        log("ERROR: RUN_MONTHS env found no months")
        exit(1)
    try:
        run_months = [int(i) for i in run_months]
    except ValueError:
        log("ERROR: faulty value in RUN_MONTHS")
        exit(1)

    #check days
    if os.environ.get('RUN_DAYS') is None:
        log("No days to run found, setting to all days")
        os.environ.setdefault('RUN_DAYS', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31')

    run_days = os.environ.get('RUN_DAYS')
    run_days = run_days.replace(' ', '').split(',')
    if len(run_days) == 0:
        log("ERROR: RUN_DAYS env found no days")
        exit(1)
    try:
        run_days = [int(i) for i in run_days]
    except ValueError:
        log("ERROR: faulty value in RUN_DAYS")
        exit(1)

    #check time
    if os.environ.get("RUN_TIME") is None:
        log("ERROR: No RUN_TIME detected")
        exit(1)
    if not len(os.environ.get("RUN_TIME")) == 5:
        log("ERROR: RUN_TIME in wrong format")
        exit(1)


if __name__ == "__main__":
    with open('VERSION', encoding="utf-8") as f:
        log("VERSION: ", f.read())

    #check environment variables
    check_env()

    if os.environ.get('UPDATE_ON_STARTUP') == 'TRUE':
        start_update()

    schedule.every().day.at(os.environ.get("RUN_TIME")).do(check_date)
    log("Schedule Started")
    while True:
        schedule.run_pending()
        time.sleep(1)
