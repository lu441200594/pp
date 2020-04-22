import os
import time
import requests


def getTime(url):
    r = requests.get(url)
    ts = r.headers.get('date')
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")  # 格式ts
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)  # +东八区
    dat = "date %u-%02u-%02u" % (ttime.tm_year, ttime.tm_mon, ttime.tm_mday)
    tm = "time %02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
    return [dat, tm]


def setTime(time):
    os.system(time[0])
    os.system(time[1])
