from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
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
    "project": "Core Platform",
    "build": "Launch Time PoC iOS",
    "name": "iPhone 13",
    "platformName": "ios",
    "platformVersion": "15",
    "deviceName": "iPhone 13",
    "browserstack.local": "true",
    "app": "bs://90d6826a222054feab0ddc887ace1c06bb99c3e5"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)

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

# actions = ActionChains(driver)
# actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
# actions.w3c_actions.pointer_action.move_to_location(192, 729)
# actions.w3c_actions.pointer_action.pointer_down()
# actions.w3c_actions.pointer_action.move_to_location(204, 447)
# actions.w3c_actions.pointer_action.release()
# actions.perform()

# action = TouchAction(driver)
# action.scroll_from_element(element, 10, 100)

# btn_perf_menu_element = WebDriverWait(driver, 30).until(
#     EC.element_to_be_clickable((MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="Performance Log"])[2]'))
# )
# btn_perf_menu_element.click()

driver.quit()
