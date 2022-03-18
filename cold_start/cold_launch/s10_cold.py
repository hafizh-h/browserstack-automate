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
    "name": "Samsung Galaxy S10 Warm",
    "platformName": "android",
    "platformVersion": "9.0",
    "deviceName": "Samsung Galaxy S10",
    "app": "bs://43d9df000cc921878557fe78d79480c0ea98c4a7"
}

des_caps_data = yaml.safe_dump(desired_caps, allow_unicode=True, default_flow_style=False, sort_keys=False)

iteration = 3

for i in range(iteration):
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

    logs = driver.get_log('logcat')
    log_messages = list(map(lambda log: log['message'], logs))

    driver.quit()

    perf_metrics = list(filter(lambda perf: 'I ActivityManager' in perf, log_messages))
    perf_file = open(desired_caps["deviceName"] + " OS " +desired_caps["platformVersion"] + " cold_perf_logs(4.31.2)-" + str(i + 1) + ".txt", "w")
    for j in perf_metrics:
        perf_file.write(j + "\n")
    perf_file.close()

    r_perf_file = open(desired_caps["deviceName"] + " OS " + desired_caps["platformVersion"] + " cold_perf_logs(4.31.2)-" + str(i + 1) + ".txt", "r")
    perf_data = r_perf_file.read()
    r_perf_file.close()

    db = MySQLdb.connect("localhost", "root", "", "automation_test")
    cursor = db.cursor()
    query = "INSERT INTO device_log (log, desired_caps) VALUES (%s, %s)"
    cursor.execute(query, (perf_data, des_caps_data))
    db.commit()
    db.close()

