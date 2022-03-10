from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess as sp
import requests
from requests.auth import HTTPBasicAuth
import time
import json
'''
Launch Time Comparison for v4.27.0 and v4.28.0
App for v4.27.0 = v4.27.0-1-RC29-HEAD-131201-release.apk
App url: bs://4ec189ab1ed759ed931c06496c848d44bf0264f4
App for v4.28.0 = v4.28.0-glideViewLoadIssue-release.apk
App url: bs://06bb5df3b27055c41e954e2e0a469c35b3f54017
App with custom tag from shasank: bs://0d1fd56d5f7dcb83210a64ed3dc36c592ae15de0
App for v4.29.0 = v4.29.0-release-4.29.0-310104-debug.apk
App url: bs://394ad5ded6384cd522fd1cf4bcfccfb19f73b16e
App for v4.30.0 = v4.30.0-release-4.30.0-150206-release.apk
App url: bs://e1cf27a39a6a15c3bec8fed938dcb71e707ea941

Current Issues:
- Can't get 'Displayed' and 'Fully drawn' from raw device logs
- The metrics can't also be found in others Android build created
  by other users
TO-DO:
- Check on how to get the metrics from the device logs in App Automate
- Explore more about python subprocess.run methods
'''
userName = "hafizh_783gSd"
accessKey = "cpKChBFWNYG4qaA4dj1H"

desired_caps = {
    "project": "Core Platform",
    "build": "Launch Time 4.29.0 Debug",
    "name": "Samsung Galaxy S21",
    "platformName": "android",
    "platformVersion": "11.0",
    "deviceName": "Samsung Galaxy S21",
    "browserstack.networkLogs": "true",
    "app": "bs://394ad5ded6384cd522fd1cf4bcfccfb19f73b16e"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)
session_id = driver.session_id

btn_cancel_element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
)
btn_cancel_element.click()

# btn_close_element = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((MobileBy.XPATH, "//android.view.View[@content-desc='light']/android.widget.Image"))
# )
# btn_close_element.click()

btn_login_menu_element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and (@text='Masuk')]"))
)
btn_login_menu_element.click()
time.sleep(45)
driver.quit()

basic = HTTPBasicAuth(userName, accessKey)
time.sleep(35) #requests had to wait ~30s because BrowserStack took some time to generate the App Profilng Data
app_profiling = requests.get('https://api.browserstack.com/app-automate/builds/c7c5c48613cb87f90f285e21b06c85725d58e841/sessions/' + str(session_id) + '/appprofiling', auth=basic)
app_start = requests.get('https://api.browserstack.com/app-automate/builds/c7c5c48613cb87f90f285e21b06c85725d58e841/sessions/' + str(session_id) + '/devicelogs', auth=basic)
app_network = requests.get('https://api.browserstack.com/app-automate/builds/c7c5c48613cb87f90f285e21b06c85725d58e841/sessions/' + str(session_id) + '/networklogs', auth=basic)

json_app_profiling = json.dumps(app_profiling.json(), indent=4, sort_keys=True)
json_file = open(desired_caps["deviceName"]+" OS "+desired_caps["platformVersion"]+" performance.json", "w")
json_file.write(json_app_profiling)
json_file.close()

app_start_file = open(desired_caps["deviceName"]+" OS "+desired_caps["platformVersion"]+" devicelogs.log", "w")
app_start_file.write(app_start.text)
app_start_file.close()

app_network_file = open(desired_caps["deviceName"]+" OS "+desired_caps["platformVersion"]+" networklogs.txt", "w")
app_network_file.write(app_network.text)
app_network_file.close()