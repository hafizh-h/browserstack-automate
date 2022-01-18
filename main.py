from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
Login Flow in GK Environment 
TO-DO:
- made implicit wait as global
  using driver.implicitly_wait(<seconds>) from appium documentation 
  causes error, maybe can't be implemented using browserstack.
  so can't declare implicitly_wait as of now, documentation from 
  browserstack only shows using WebDriverWait for every element
'''
userName = "hafizh_783gSd"
accessKey = "cpKChBFWNYG4qaA4dj1H"

desired_caps = {
    "project": "Samsung A51",
    "build": "Android",
    "name": "login_flow_gk",
    "platformName": "android",
    "platformVersion": "10.0",
    "device": "Samsung Galaxy A51",
    "browserstack.local": "true",
    "app": "bs://99969ffbc85c2582ec69e622464fce94adbcab05"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)

btn_cancel_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
)
btn_cancel_element.click()

btn_login_menu_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and (@text='Masuk')]"))
)
btn_login_menu_element.click()

email_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ID, "com.tiket.gits.debug:id/tds_box_input_text"))
)
email_input.send_keys("testing.aut.loyalty1@gmail.com")

btn_next_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ID, "com.tiket.gits.debug:id/btn_one_field"))
)
btn_next_element.click()

password_input = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_box_input_text') and (@text='Kata Sandi') or (@text='Password')]"))
)
password_input.send_keys("Testingdev123!")

btn_submit_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ID, "com.tiket.gits.debug:id/btn_submit"))
)
btn_submit_element.click()

otp1_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'et_otp_1')]//android.widget.EditText"))
)
otp1_element.send_keys("1")

otp2_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'et_otp_2')]//android.widget.EditText"))
)
otp2_element.send_keys("2")

otp3_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'et_otp_3')]//android.widget.EditText"))
)
otp3_element.send_keys("3")

otp4_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'et_otp_4')]//android.widget.EditText"))
)
otp4_element.send_keys("4")

close_bio_el = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ID, "com.tiket.gits.debug:id/iv_close"))
)
close_bio_el.click()

driver.quit()
