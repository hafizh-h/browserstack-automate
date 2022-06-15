import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

userName = "hafizh_783gSd"
accessKey = "cpKChBFWNYG4qaA4dj1H"

desired_caps = {
    "project": "Core Platform",
    "build": "Launch Time 4.33.0-FeatureBuild",
    "name": "Samsung Galaxy S9 Warm",
    "platformName": "android",
    "platformVersion": "8.0",
    "deviceName": "Samsung Galaxy S9",
    "app": "bs://f7781a9817de97e7716577272f691b83a8499f3f"
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

    # btn_login_menu_element = wait.until(
    #     ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
    #                                                 "@text='Masuk')]"))
    # )
    # btn_login_menu_element.click()

    driver.close_app()
    time.sleep(5)

    driver.launch_app()

    btn_cancel_element = wait.until(
        ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
    )
    btn_cancel_element.click()

    # btn_login_menu_element = wait.until(
    #     ec.element_to_be_clickable((MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
    #                                                 "@text='Masuk')]"))
    # )
    # btn_login_menu_element.click()

    logs = driver.get_log('logcat')
    log_messages = list(map(lambda log: log['message'], logs))

    driver.quit()

    perf_metrics = list(
        filter(lambda perf: 'I ActivityManager' in perf, log_messages))

    displayed_metrics = list(
        filter(lambda disp: 'Displayed com.tiket.gits/.v2splash.SplashV2Activity' in disp, perf_metrics))
    fd_metrics = list(filter(lambda fd: 'Fully drawn com.tiket.gits/.v2splash.SplashV2Activity' in fd, perf_metrics))

    warm_displayed = displayed_metrics[1:]
    warm_fully_drawn = fd_metrics[1:]

    conv_displayed = "".join(warm_displayed)
    conv_fully_drawn = "".join(warm_fully_drawn)

    sliced_displayed = conv_displayed[103:]
    sliced_fully_drawn = conv_fully_drawn[105:]

    log_metrics = displayed_metrics + fd_metrics

    log_file = open(
        desired_caps["deviceName"] + " OS " + desired_caps["platformVersion"] + " warm_perf_logs(FeatureBuild)-" + str(
            i + 1) + ".txt", "w")
    for j in log_metrics:
        log_file.write(j + "\n")
    log_file.close()