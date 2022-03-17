import time
import yaml
import MySQLdb
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

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

des_caps = yaml.safe_dump(desired_caps, allow_unicode=True, default_flow_style=False, sort_keys=False)

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

# insert perf_file to database
perf_log_file = open(desired_caps["deviceName"] + " OS "+desired_caps["platformVersion"] + " perf_logs.txt", "r")
perf_log_content = perf_log_file.read()
perf_log_file.close()

db = MySQLdb.connect("localhost","root","","automation_test")
cursor = db.cursor()
query = "INSERT INTO device_log (log, desired_caps) VALUES (%s, %s)"
cursor.execute(query, (perf_log_content, des_caps))
db.commit()
db.close()