from appium import webdriver
import subprocess as sp

'''
Launch Time Comparison for v4.27.0 and v4.28.0
App for v4.27.0 = v4.27.0-1-RC29-HEAD-131201-release.apk
App url: bs://4ec189ab1ed759ed931c06496c848d44bf0264f4
App for v4.28.0 = v4.28.0-glideViewLoadIssue-release.apk
App url: bs://06bb5df3b27055c41e954e2e0a469c35b3f54017

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
    "build": "Launch Time Comparison",
    "name": "launch_time_4.27.0",
    "platformName": "android",
    "platformVersion": "11.0",
    "deviceName": "Samsung Galaxy S21",
    "app": "bs://4ec189ab1ed759ed931c06496c848d44bf0264f4"
}

driver = webdriver.Remote("https://" + userName + ":" + accessKey + "@hub-cloud.browserstack.com/wd/hub", desired_caps)
driver.implicitly_wait(20)
# test = sp.run(["adb logcat -d | grep 'Displayed com.tiket.gits' | sed '1q;d'| awk '{print $5, $7}'"], text=True, shell=True)
# print(test)

# displayed = sp.run(["adb logcat -d | grep 'Displayed com.tiket.gits/.v2splash.SplashV2Activity' | sed '1q;d' | awk '{"
#                     "print $7, $9}'"], text=True, shell=True)
# print(displayed)

driver.quit()
