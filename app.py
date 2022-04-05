import re
import time
import MySQLdb
import statistics
from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from werkzeug.utils import redirect

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'okta.salsabila@tiket.com'
app.config['MAIL_PASSWORD'] = 'ypjjxpbyrnhelgyd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def convert_time_to_float(str):
    time = list(map(int, re.split('[sm]', str)[:-2]))
    if len(time) == 2:
        return time[0] + time[1]*0.001
    else:
        return time[0]*0.001

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/results/<id>',methods=['GET','POST'])
def results(id):
    db = MySQLdb.connect("localhost", "root", "", "db_automation_test")
    cur = db.cursor()
    cur.execute("SELECT * FROM device_log WHERE id = " + id)
    data = cur.fetchall()
    return render_template("results.html",data=data)

@app.route('/reports',methods=['GET','POST'])
def reports():
    db = MySQLdb.connect("localhost", "root", "", "db_automation_test")
    cur = db.cursor()
    cur.execute("SELECT * FROM device_log")
    data = cur.fetchall()
    return render_template("reports.html",data=data)

@app.route('/testing', methods=['POST', 'GET'])
def testing():
    userName = "hafizh_783gSd"
    accessKey = "cpKChBFWNYG4qaA4dj1H"

    if request.method == 'POST':
        build = request.form['build']
        name = request.form['name']
        platformName = request.form['platformName']
        platformVersion = request.form['platformVersion']
        deviceName = request.form['deviceName']
        app = request.form['app']
        networkProfile = request.form['networkProfile']
        iteration = int(request.form['iteration'])
        type = request.form['type']

        desired_caps = {
            "project": "Core Platform",
            "build": build,
            "name": name,
            "platformName": platformName,
            "platformVersion": platformVersion,
            "deviceName": deviceName,
            "app": app,
            "networkProfile": networkProfile
        }

        displayed_time = []
        fully_drawn_time = []

        if type == "cold":
            for i in range(iteration):
                driver = webdriver.Remote(
                    "https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)
                session_id = driver.session_id
                wait = WebDriverWait(driver, 10)

                btn_cancel_element = wait.until(
                    ec.element_to_be_clickable(
                        (MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
                )
                btn_cancel_element.click()

                btn_login_menu_element = wait.until(
                    ec.element_to_be_clickable(
                        (MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
                                         "@text='Masuk')]"))
                )
                btn_login_menu_element.click()

                logs = driver.get_log('logcat')
                log_messages = list(map(lambda log: log['message'], logs))

                driver.quit()

                if (float(platformVersion) >= 10.0):
                    perf_metrics = list(
                        filter(lambda perf: 'I ActivityTaskManager' in perf, log_messages))
                else:
                    perf_metrics = list(
                        filter(lambda perf: 'I ActivityManager' in perf, log_messages))

                displayed_metrics = list(
                    filter(lambda disp: 'Displayed com.tiket.gits/.v2splash.SplashV2Activity' in disp, perf_metrics))
                fd_metrics = list(
                    filter(lambda fd: 'Fully drawn com.tiket.gits/.v2splash.SplashV2Activity' in fd, perf_metrics))

                conv_displayed = "".join(displayed_metrics)
                conv_fully_drawn = "".join(fd_metrics)

                if (float(platformVersion) >= 10.0):
                    sliced_displayed = conv_displayed[108:]
                    sliced_fully_drawn = conv_fully_drawn[110:]
                else:
                    sliced_displayed = conv_displayed[104:]
                    sliced_fully_drawn = conv_fully_drawn[106:]

                split_displayed = [item.split() for item in "".join(sliced_displayed).split('(') if item]
                str_displayed = ''.join([str(elem) for elem in split_displayed[0]])

                split_fully_drawn = [item.split() for item in "".join(sliced_fully_drawn).split('(') if item]
                str_fully_drawn = ''.join([str(elem) for elem in split_fully_drawn[0]])

                float_displayed = convert_time_to_float(str_displayed)
                float_fully_drawn = convert_time_to_float(str_fully_drawn)

                log_metrics = displayed_metrics + fd_metrics

                log_file = open(
                    desired_caps["deviceName"] + " OS " + desired_caps[
                        "platformVersion"] + " cold_perf_logs(4.31.2)-" + str(
                        i + 1) + ".txt", "w")
                for j in log_metrics:
                    log_file.write(j + "\n")
                log_file.close()

                displayed_time.append(float_displayed)
                fully_drawn_time.append(float_fully_drawn)

        elif type == "warm":
            for i in range(iteration):
                driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub",
                                          desired_caps)
                session_id = driver.session_id
                wait = WebDriverWait(driver, 10)

                btn_cancel_element = wait.until(
                    ec.element_to_be_clickable(
                        (MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
                )
                btn_cancel_element.click()

                btn_login_menu_element = wait.until(
                    ec.element_to_be_clickable(
                        (MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
                                         "@text='Masuk')]"))
                )
                btn_login_menu_element.click()

                driver.close_app()
                time.sleep(5)

                driver.launch_app()

                btn_cancel_element = wait.until(
                    ec.element_to_be_clickable(
                        (MobileBy.XPATH, "//*[contains(@resource-id, 'tds_btn') and (@text='Batalkan')]"))
                )
                btn_cancel_element.click()

                btn_login_menu_element = wait.until(
                    ec.element_to_be_clickable(
                        (MobileBy.XPATH, "//*[contains(@resource-id, 'tds_title_bottom_navigation') and ("
                                         "@text='Masuk')]"))
                )
                btn_login_menu_element.click()

                logs = driver.get_log('logcat')
                log_messages = list(map(lambda log: log['message'], logs))

                driver.quit()

                if (float(platformVersion) >= 10.0):
                    perf_metrics = list(
                        filter(lambda perf: 'I ActivityTaskManager' in perf, log_messages))
                else:
                    perf_metrics = list(
                        filter(lambda perf: 'I ActivityManager' in perf, log_messages))

                displayed_metrics = list(
                    filter(lambda disp: 'Displayed com.tiket.gits/.v2splash.SplashV2Activity' in disp, perf_metrics))
                fd_metrics = list(
                    filter(lambda fd: 'Fully drawn com.tiket.gits/.v2splash.SplashV2Activity' in fd, perf_metrics))

                warm_displayed = displayed_metrics[1:]
                warm_fully_drawn = fd_metrics[1:]

                conv_displayed = "".join(warm_displayed)
                conv_fully_drawn = "".join(warm_fully_drawn)

                if (float(platformVersion) >= 10.0):
                    sliced_displayed = conv_displayed[108:]
                    sliced_fully_drawn = conv_fully_drawn[110:]
                else:
                    sliced_displayed = conv_displayed[104:]
                    sliced_fully_drawn = conv_fully_drawn[106:]

                split_displayed = [item.split() for item in "".join(sliced_displayed).split('(') if item]
                str_displayed = ''.join([str(elem) for elem in split_displayed[0]])

                split_full_drawn = [item.split() for item in "".join(sliced_fully_drawn).split('(') if item]
                str_fully_drawn = ''.join([str(elem) for elem in split_full_drawn[0]])

                float_displayed = convert_time_to_float(str_displayed)
                float_fully_drawn = convert_time_to_float(str_fully_drawn)

                log_metrics = displayed_metrics + fd_metrics

                log_file = open(
                    desired_caps["deviceName"] + " OS " + desired_caps[
                        "platformVersion"] + " warm_perf_logs(4.31.2)-" + str(
                        i + 1) + ".txt", "w")
                for j in log_metrics:
                    log_file.write(j + "\n")
                log_file.close()

                displayed_time.append(float_displayed)
                fully_drawn_time.append(float_fully_drawn)

        displayed_avg = statistics.mean(displayed_time)
        fully_drawn_avg = statistics.mean(fully_drawn_time)

        db = MySQLdb.connect("localhost", "root", "", "db_automation_test")
        cursor = db.cursor()

        columns = ', '.join("`" + str(x) + "`" for x in desired_caps.keys())
        values = ', '.join("'" + str(x) + "'" for x in desired_caps.values())
        insert_sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('device_log', columns, values)
        cursor.execute(insert_sql)
        id = int(cursor.lastrowid)
        db.commit()

        update_sql = "UPDATE %s SET displayed_avg = %f, fully_drawn_avg = %f, type = '%s', iteration = %d WHERE id = %d" % (
            'device_log', displayed_avg, fully_drawn_avg, type, iteration, id)
        cursor.execute(update_sql)
        db.commit()
        db.close()

        msg = Message(
            'Automation Testing Results',
            sender='okta.salsabila@tiket.com',
            recipients=['minochndk@gmail.com', 'chandika.salsabila@gmail.com']
        )

        msg.body = 'Redirect to this URL: http://localhost:5000/results/' + str(id)
        mail.send(msg)

        return redirect(url_for('results', id=id))

if __name__ == "__main__":
    app.run(debug = True)