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
    "name": "Samsung Galaxy S10 Cold",
    "platformName": "android",
    "platformVersion": "9.0",
    "deviceName": "Samsung Galaxy S10",
    "app": "bs://43d9df000cc921878557fe78d79480c0ea98c4a7"
}

iteration = 10

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

    perf_metrics = list(
        filter(lambda perf: 'I ActivityManager' in perf, log_messages))

    displayed_metrics = list(
        filter(lambda disp: 'Displayed com.tiket.gits/.v2splash.SplashV2Activity' in disp, perf_metrics))
    fd_metrics = list(filter(lambda fd: 'Fully drawn com.tiket.gits/.v2splash.SplashV2Activity' in fd, perf_metrics))

    conv_displayed = "".join(displayed_metrics)
    conv_fully_drawn = "".join(fd_metrics)

    sliced_displayed = conv_displayed[103:]
    sliced_fully_drawn = conv_fully_drawn[105:]

    perf_file = open(
        desired_caps["deviceName"] + " OS " + desired_caps["platformVersion"] + " cold_perf_logs(4.31.2)-" + str(
            i + 1) + ".txt", "w")
    for j in perf_metrics:
        perf_file.write(j + "\n")
    perf_file.close()

    db = MySQLdb.connect("localhost", "root", "", "automation_test")
    cursor = db.cursor()

    columns = ', '.join("`" + str(x) + "`" for x in desired_caps.keys())
    values = ', '.join("'" + str(x) + "'" for x in desired_caps.values())
    insert_sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('device_log', columns, values)
    cursor.execute(insert_sql)
    db.commit()

    update_sql = "UPDATE %s SET displayed = '%s', fully_drawn = '%s' ORDER BY id DESC LIMIT 1" % (
    'device_log', sliced_displayed, sliced_fully_drawn)
    cursor.execute(update_sql)
    db.commit()
    db.close()