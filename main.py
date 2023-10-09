
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("Test Execution Started")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
with webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                      options=options
                      ) as driver:

    #maximize the window size
    driver.maximize_window()
    time.sleep(0.5)
    #navigate to browserstack.com
    driver.get("http://192.168.2.115:6052/")
    time.sleep(1)

    try:
        sroot = driver.find_element(By.XPATH, "//header/esphome-header-menu").shadow_root
        print("found shadowroot")
        sroot.find_element(By.CSS_SELECTOR, "mwc-button").click()
        time.sleep(5)
        
        esphomeconfdia = driver.find_element(By.XPATH, "//esphome-confirmation-dialog").shadow_root
        dialog = esphomeconfdia.find_element(By.CSS_SELECTOR, "mwc-dialog")
        dialog.find_element(By.XPATH, "mwc-button[2]").click()

    except Exception as e:
        print(e)
    time.sleep(10)

    

 
print("Test Execution Successfully Completed!")