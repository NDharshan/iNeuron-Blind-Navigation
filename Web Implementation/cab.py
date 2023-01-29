from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



def book_a_cab():
        
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications" : 1, "profile.default_content_setting_values.geolocation": 1}

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://book.olacabs.com/?pickup_name=Current%20Location&lat=13.0540663&lng=77.7614751")
    time.sleep(2)

    # location_button=driver.find_element('xpath','/html/body/ola-app//iron-pages/ola-home//ola-loc-permission//div/div/div[2]/button')
    # location_button=driver.find_element(By.XPATH, "/html/body/ola-app//iron-pages/ola-home//ola-loc-permission//div/div/div[2]/button")
    # location_button=driver.find_elements("xpath","//*[contains(text(), 'Continue to next step')]")
    # print(location_button[0].text())
    # locatoin_button[0].click()
    # /html/body/ola-app//iron-pages/ola-home//ola-loc-permission//div/div/div[2]/button


    # element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "/div/div/div[3]"))
    #     )
    # drop_location=driver.find_element('xpath','/div/div/div[3]')
    # time.sleep(5)
    driver.quit()
    # /div/div/div[3]
    # driver.quit()