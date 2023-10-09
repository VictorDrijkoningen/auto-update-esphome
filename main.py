
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, datetime
import os
import schedule

def update_esphome(esphometarget, seleniumtarget):
    print("Starting ESPHOME Update All")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    with webdriver.Remote(command_executor='http://'+seleniumtarget+'/wd/hub',
                        options=options
                        ) as driver:

        #maximize the window size
        driver.maximize_window()
        time.sleep(0.5)

        driver.get('http://'+esphometarget)
        time.sleep(1)

        try:
            #press first update_all button
            driver.find_element(By.XPATH, "//esphome-header-menu").shadow_root.find_element(By.CSS_SELECTOR, "mwc-button").click()
            time.sleep(5)
            #press second update_all button in dialog
            driver.find_element(By.XPATH, "//esphome-confirmation-dialog").shadow_root.find_element(By.CSS_SELECTOR, "mwc-dialog").find_element(By.XPATH, "mwc-button[2]").click()

        except Exception as e:
            print(e)
        time.sleep(1000)

def job():
    if datetime.date.today().day not in [9]:
        print("Not today m'dude", datetime.date.today().day)
        return
    #check environ:
    #TODO

    update_esphome(os.environ['ESPHOME_TARGET'], os.environ['SELENIUM_TARGET'])

if __name__ == "__main__":
    schedule.every().day.at("01:00").do(job)
    print("Schedule Started")

    #TODO check esp en selenium target


    while True:
        schedule.run_pending()
        time.sleep(1)
    
