# Fix issue with wrong timezone in pythonanywhere web app*/
# Source: https://help.pythonanywhere.com/pages/SettingTheTimezone
import os
import time
from sys import platform


def setTimeZone(timezone: str = "Asia/Kolkata"):
    os.environ["TZ"] = timezone  # define TZ environment variable
    if platform != "win32":
        time.tzset()  # set the timezone
        # tzset() will only work if platform is not Windows.
