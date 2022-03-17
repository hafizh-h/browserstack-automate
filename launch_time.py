from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.auth import HTTPBasicAuth
import time
import json

userName = "hafizh_783gSd"
accessKey = "cpKChBFWNYG4qaA4dj1H"

desired_caps = {
    "project": "Core Platform",
    "build": "Launch Time Comparison",
    "name": "launch_time_4.27.0",
    "platformName": "android",
    "platformVersion": "11.0",
    "deviceName": "Samsung Galaxy S21",
    "app": "bs://0d1fd56d5f7dcb83210a64ed3dc36c592ae15de0"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)
session_id = driver.session_id

# test = sp.run(["adb logcat -d | grep 'Displayed com.tiket.gits' | sed '1q;d'| awk '{print $5, $7}'"], text=True, shell=True)
# print(test)

# displayed = sp.run(["adb logcat -d | grep 'Displayed com.tiket.gits/.v2splash.SplashV2Activity' | sed '1q;d' | awk '{"
#                     "print $7, $9}'"], text=True, shell=True)
# print(displayed)

btn_cancel_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
)
btn_cancel_element.click()

btn_close_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.View[@content-desc='light']/android.widget.Image"))
)
btn_close_element.click()

btn_login_menu_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and (@text='Masuk')]"))
)
btn_login_menu_element.click()

time.sleep(45)
driver.quit()

basic = HTTPBasicAuth(userName, accessKey)
time.sleep(35) #requests had to wait ~30s because BrowserStack took some time to generate the App Profilng Data
app_profiling = requests.get('https://api.browserstack.com/app-automate/builds/0cf20a8dfbaa3208b41a29b0b9c03482664ccf02/sessions/' + str(session_id) + '/appprofiling', auth=basic)
app_start = requests.get('https://api.browserstack.com/app-automate/builds/0cf20a8dfbaa3208b41a29b0b9c03482664ccf02/sessions/' + str(session_id) + '/devicelogs', auth=basic)

json_app_profiling = json.dumps(app_profiling.json(), indent=4, sort_keys=True)
json_file = open(desired_caps["deviceName"]+" OS "+desired_caps["platformVersion"]+" performance.json", "w")
json_file.write(json_app_profiling)
json_file.close()

app_start_file = open(desired_caps["deviceName"]+" OS "+desired_caps["platformVersion"]+" devicelogs.log", "w")
app_start_file.write(app_start.text)
app_start_file.close()

