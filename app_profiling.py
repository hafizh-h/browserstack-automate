import requests
from requests.auth import HTTPBasicAuth
'''
TO-DO:
* Search for a way to automatically get buildID and sessionID for deviceLogs and appprofiling
* URL for Device Logs: https://api.browserstack.com/app-automate/builds/{buildID}/sessions/{sessionID}/devicelogs
* URL for App Profiling: https://api.browserstack.com/app-automate/builds/{buildID}/sessions/{sessionID}/appprofiling
'''
basic = HTTPBasicAuth('hafizh_783gSd', 'cpKChBFWNYG4qaA4dj1H')
r = requests.get('https://api.browserstack.com/app-automate/builds/0cf20a8dfbaa3208b41a29b0b9c03482664ccf02/sessions'
                 '/5885820a0056ea260395583ef1feb7739d0694aa/appprofiling', auth=basic)

print(r.json())
