
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, datetime
import os
import schedule
import re

def update_esphome_via_selenium(esphometarget):
    print("Starting ESPHOME Update All")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    with webdriver.Chrome() as driver:

        driver.maximize_window()
        time.sleep(0.5)

        driver.get('http://'+esphometarget)
        time.sleep(2)

        try:
            #press first update_all button
            driver.find_element(By.XPATH, "//esphome-header-menu").shadow_root.find_element(By.CSS_SELECTOR, "mwc-button").click()
            time.sleep(2)
            #press second update_all button in dialog
            driver.find_element(By.XPATH, "//esphome-confirmation-dialog").shadow_root.find_element(By.CSS_SELECTOR, "mwc-dialog").find_element(By.XPATH, "mwc-button[2]").click()

        except Exception as e:
            print(e)
        
        #wait for alle esp devices to be updated
        time.sleep(1000)


def update_esphome_via_socket(esphometarget):
    pass


def job():
    if datetime.date.today().day not in [15]:
        print("Not today m'dude", datetime.date.today().day)
        return

    if os.environ['MODE'] == 'selenium':
        update_esphome_via_selenium(os.environ['ESPHOME_TARGET'])
    elif os.environ['MODE'] == 'socket':
        update_esphome_via_socket(os.environ['ESPHOME_TARGET'])
    else:
        print("How did we get here?")
        exit(1)



def check_env():
    '''function checks the environment variables to be suitable for this code'''

    ip_regex = r'[0-9]+(?:\.[0-9]+){3}:[0-9]+' #TODO include ipv6, but good enough for now.

    if os.environ.get('MODE') != 'selenium' and os.environ.get('MODE') != 'socket':
        print("ERROR: unknown mode")
        exit(1)

    if not re.search(ip_regex, str(os.environ.get('ESPHOME_TARGET'))):
        print("ERROR: esphome target not valid")
        exit(1)
    


if __name__ == "__main__":
    '''main program thread'''

    #check environment variables
    check_env()

    job()
    schedule.every().day.at("19:00").do(job)
    print("Schedule Started")
    while True:
        schedule.run_pending()
        time.sleep(1)
    
