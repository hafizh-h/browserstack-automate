import time

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
App for v4.31.2 Release = v4.31.2-RC111-HEAD-020312-release.apk
App url: bs://43d9df000cc921878557fe78d79480c0ea98c4a7
App for v4.32.0 Release = v4.32.0-RC119-HEAD-090310-release.apk
App url: bs://743efc2e4e1a72a41bfd1eb69b50b59321063aba
'''
userName = "hafizh_783gSd"
accessKey = "cpKChBFWNYG4qaA4dj1H"

desired_caps = {
    "project": "Core Platform",
    "build": "Launch Time 4.31.2 Release",
    "name": "Samsung Galaxy S21 Cold 1",
    "platformName": "android",
    "platformVersion": "11.0",
    "deviceName": "Samsung Galaxy S21",
    "app": "bs://43d9df000cc921878557fe78d79480c0ea98c4a7"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)
session_id = driver.session_id

wait = WebDriverWait(driver, 10)

btn_cancel_element = wait.until(
    ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
)
btn_cancel_element.click()

btn_close_element = wait.until(
    ec.element_to_be_clickable((MobileBy.XPATH, "//android.view.View[@content-desc='light']/android.widget.Image"))
)
btn_close_element.click()

btn_login_menu_element = wait.until(
    ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
                                                "@text='Masuk')]"))
)
btn_login_menu_element.click()

driver.close_app()
time.sleep(5)
driver.launch_app()

btn_cancel_element = wait.until(
    ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
)
btn_cancel_element.click()

btn_close_element = wait.until(
    ec.element_to_be_clickable((MobileBy.XPATH, "//android.view.View[@content-desc='light']/android.widget.Image"))
)
btn_close_element.click()

btn_login_menu_element = wait.until(
    ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
                                                "@text='Masuk')]"))
)
btn_login_menu_element.click()

logs = driver.get_log('logcat')
log_messages = list(map(lambda log: log['message'], logs))

driver.quit()

log_file = open(desired_caps["deviceName"] + " OS "+desired_caps["platformVersion"] + " logs.txt", "w")
for i in log_messages:
    log_file.write(i + "\n")
log_file.close()

perf_metrics = list(filter(lambda perf: 'I ActivityTaskManager' in perf, log_messages))

perf_file = open(desired_caps["deviceName"] + " OS "+desired_caps["platformVersion"] + " perf_logs.txt", "w")
for j in perf_metrics:
    perf_file.write(j + "\n")
perf_file.close()
