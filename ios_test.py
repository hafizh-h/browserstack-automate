from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

userName = "oktachandikasals_Vs7YaH"
accessKey = "zJc9cFuGz5wiJN8tvue4"

desired_caps = {
    "project": "Core Platform",
    "build": "Launch Time PoC iOS Test",
    "name": "iPhone 13",
    "platformName": "ios",
    "platformVersion": "15",
    "deviceName": "iPhone 13",
    "app": "bs://4ab38ea18799d668ba92da6fafd3d970757729cd"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)
session_id = driver.session_id

btn_allow_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, '//XCUIElementTypeButton[@name="Allow"]'))
)
btn_allow_element.click()

btn_allow2_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, '//XCUIElementTypeButton[@name="Allow"]'))
)
btn_allow2_element.click()

btn_login_menu_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.XPATH, '//XCUIElementTypeButton[@name="Masuk"]'))
)
btn_login_menu_element.click()

btn_more_menu_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((MobileBy.ID, 'tds ic more horizontal'))
)
btn_more_menu_element.click()

driver.execute_script('mobile: scroll', {'direction': 'down'})
driver.find_element(MobileBy.ACCESSIBILITY_ID, 'PerformanceLog').click()

perf = driver.find_element(MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeTextView[4]')
perf_metrics = perf.get_attribute("value")
print(perf_metrics)

driver.quit()

app_start_file = open(desired_caps["deviceName"]+" OS "+desired_caps["platformVersion"]+".txt", "w")
app_start_file.write(perf_metrics)
app_start_file.close()
