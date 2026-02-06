import os
import platform
import time
import datetime
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import schedule
from helpers import check_config_dir, trim_log, log, check_geckodriver, check_env, save_screenshot

CONFIGDIR = "/config/"
DRIVERTAR = "/config/driver/download.tar.gz"
DRIVERDIR = "/config/driver/"
LINKAARCH64DRIVER = "https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux-aarch64.tar.gz"
DRIVERVERSION="0.36.0"
LOGFILE = "/config/app.log"


def update_esphome_via_selenium(driver, esphometarget, authentication = None):
    '''update esphome devices via a selenium operated firefox instance'''

    driver.maximize_window()
    driver.get('http://'+esphometarget)
    time.sleep(5)

    try:
        if not (authentication is None or authentication == [None, None] ):
            #There is authentication needed
            save_screenshot(CONFIGDIR, driver, "1.beforeauth")
            el = "username-field"
            input_username = driver.find_element(By.ID , el)
            input_username.send_keys(authentication[0])
            el = "password-field"
            input_username = driver.find_element(By.ID , el)
            input_username.send_keys(authentication[1])
            save_screenshot(CONFIGDIR, driver, "2.aftertyping")
            el = "login-form-submit"
            input_submit = driver.find_element(By.ID, el)
            input_submit.click()
            save_screenshot(CONFIGDIR, driver, "3.afterauth")

        time.sleep(10) #wait for page-load

        try:
            el = "login-form-submit"
            ans_loggedin = driver.find_element(By.ID, el)
            log(LOGFILE, f"ERROR: LOGIN FAILED, {ans_loggedin}, Wrong password or username?")
            return 2
        except selenium.common.exceptions.NoSuchElementException:
            log(LOGFILE, "Successfully logged in")

        #check if devices are up-to-date
        el = "//esphome-devices-list"
        devices_list = driver.find_element(By.XPATH, el).shadow_root
        el = "esphome-configured-device-card"
        devices = devices_list.find_elements(By.CSS_SELECTOR, el)
        found_updateable = False
        updateable_devices = 0
        for device in devices:
            card = device.shadow_root.find_element(By.CSS_SELECTOR, 'esphome-card')
            status = card.find_elements(By.XPATH, "//div[@class='tooltip-container']")

            if len(status) > 0:
                found_updateable = True
                updateable_devices += 1

        if not found_updateable:
            log(LOGFILE, "no updates found for devices, done updating")
            return 1

        log(LOGFILE, f"Found {updateable_devices} devices that can be updated")


        #press first update_all button
        el = "//esphome-header-menu"
        button_encasing = driver.find_element(By.XPATH, el).shadow_root
        el = "mwc-button"
        button_encasing.find_element(By.CSS_SELECTOR, el).click()
        save_screenshot(CONFIGDIR, driver, "4.dialog")


        time.sleep(2)

        #press second update_all button in dialog
        el = "update-confirmation-dialog"
        dialog = driver.find_element(By.XPATH, "//esphome-confirmation-dialog").shadow_root
        button_encasing = dialog.find_element(By.CSS_SELECTOR, "mwc-dialog")
        button_encasing.find_element(By.XPATH, "mwc-button[2]").click()

        #wait for all esp devices to be updated
        log(LOGFILE, "waiting for update to finish")

        #wait for summary to appear or timeout this action
        starttime = time.time()
        oldpage = driver.get_screenshot_as_base64()
        screenshotcount = 0
        compiletimeout = (3600 if os.environ.get("COMPILE_TIMEOUT") is None else int(os.environ.get("COMPILE_TIMEOUT")))

        while True:
            time.sleep(compiletimeout/60)
            screenshotcount += 1
            save_screenshot(CONFIGDIR, driver, f"4.{screenshotcount}-{time.time() - starttime}updateprocess")

            if time.time() - starttime > compiletimeout:
                log(LOGFILE, "ERROR: timeout... update failed?")
                save_screenshot(CONFIGDIR, driver, "5.failed")
                break

            #compare page to see if nothing is changing anymore
            newpage = driver.get_screenshot_as_base64()
            if newpage == oldpage:
                log(LOGFILE, f"end of update detected, took {round(time.time()-starttime)} seconds")
                save_screenshot(CONFIGDIR, driver, "5.success")
                break
            oldpage = newpage

    except selenium.common.exceptions.NoSuchElementException as e:
        log(LOGFILE, f"Some elements could not be found in esphome {e}")
        log(LOGFILE, f"element: {el}")
        log(LOGFILE, "ERROR: ESPHOME UPDATING FAILED")
    return 0


def update_esphome_via_socket(esphometarget, auth):
    '''Update esphome devices via a socket call'''
    log(LOGFILE, "TODO socket call implementation")
    exit(1)


def start_update():
    '''start the update process'''
    log(LOGFILE, "Starting ESPHOME Update All")
    
    auth = [os.environ.get('USERNAME'), os.environ.get('PASSWORD')]
    if os.environ['MODE'] == 'selenium':
        if platform.machine() == "aarch64":
            print("running with arm64 binary")
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            service = webdriver.FirefoxService(executable_path=DRIVERDIR+"geckodriver")
            with webdriver.Firefox(service=service, options=opts) as driver:
                update_esphome_via_selenium(driver, os.environ['ESPHOME_TARGET'], auth)
        else:
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            with webdriver.Firefox(options=opts) as driver:
                update_esphome_via_selenium(driver, os.environ['ESPHOME_TARGET'], auth)

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


if __name__ == "__main__":
    print("Auto update esphome! \nQuestions? https://github.com/VictorDrijkoningen/auto-update-esphome")
    check_config_dir(CONFIGDIR, LOGFILE)
    trim_log(LOGFILE)

    with open('VERSION', encoding="utf-8") as f:
        log(LOGFILE, f"VERSION: {f.read()}")

    check_env(LOGFILE)
    check_geckodriver(LOGFILE, DRIVERDIR, DRIVERTAR, LINKAARCH64DRIVER, DRIVERVERSION)

    if os.environ.get('UPDATE_ON_STARTUP').lower() == 'true':
        start_update()

    schedule.every().day.at(os.environ.get("RUN_TIME"), os.environ.get("TIMEZONE")).do(check_date)
    log(LOGFILE, "Schedule Started")
    while True:
        schedule.run_pending()
        time.sleep(30)
