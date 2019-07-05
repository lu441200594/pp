import time
import os
import threading
from selenium import webdriver
from PIL import Image
import logging
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import baidu_ocr
import configparser
from selenium.webdriver.common.action_chains import ActionChains
from pynput import keyboard
import traceback
import re
from io import BytesIO
import sys
import opencv_util

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log/log-' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d') + '.txt',
                    filemode='a')

cf = configparser.ConfigParser()
cf.read('resource/default.conf', encoding='UTF-8')

infoLoc = cf['infoLoc']
infoLeft = infoLoc['left']
infoTop = infoLoc['top']
infoRight = infoLoc['right']
infoBottom = infoLoc['bottom']

bidLoc = cf['bidLoc']
bidX = int(bidLoc['x'])
bidY = int(bidLoc['y'])

priceLoc = cf['priceLoc']
priceX = int(priceLoc['x'])
priceY = int(priceLoc['y'])

pricePlusLoc = cf['pricePlusLoc']
pricePlusX = int(pricePlusLoc['x'])
pricePlusY = int(pricePlusLoc['y'])
pricePlusEnterX = int(pricePlusLoc['enterX'])
pricePlusEnterY = int(pricePlusLoc['enterY'])

plus300Loc = cf['plus300Loc']
plus300X = int(plus300Loc['x'])
plus300Y = int(plus300Loc['y'])

# confirmLoc = cf['confirmLoc']
# confirmX = int(confirmLoc['x'])
# confirmY = int(confirmLoc['y'])

yzmEnterLoc = cf['yzmEnterLoc']
yzmEnterX = int(yzmEnterLoc['x'])
yzmEnterY = int(yzmEnterLoc['y'])

bidTime = cf['bidTime']
secondSec = bidTime['secondSec']
thirdSec = bidTime['thirdSec']
testMin = int(bidTime['testMin'])

forceBid = cf['forceBid']
ifForceBid = forceBid.getboolean('ifForceBid')
forceBidMillis = float(forceBid['forceBidMillis'])

bidPrice = cf['price']
secondPrice = bidPrice['secondPrice']
thirdPrice = bidPrice['thirdPrice']
liePrice = bidPrice['liePrice']
diff = bidPrice['diff']
ifSavePrice = bidPrice.getboolean('ifSavePrice')

curPrice = '0'

lock = threading.Lock()
thread_lock = threading.Lock()

infoDir = {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}
webDir = {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}


def pp():
    # 关键操作需截图
    try:
        # url = 'http://test.alltobid.com/moni/gerenlogin.html'
        url = 'https://paimai2.alltobid.com/bid/'
        # url = 'https://www.baidu.com'
        path = os.path.join(os.getcwd(), 'resource')
        os.environ['PATH'] += '{}{}{}'.format(os.pathsep, path, os.pathsep)

        # 判断保护模式，win10的ie11需将http://localhost加入到白名单

        driver = webdriver.Ie()
        driver.implicitly_wait(1)
        driver.maximize_window()
        # driver.set_window_size(800, 720)
        driver.get(url)
        time.sleep(1)

        # 配置参数

        # 11:29:00开始记录当前价
        scheduler = BlockingScheduler()
        # scheduler.add_job(func=begin, args=(driver,), trigger='interval', seconds=20)
        if testMin == -1:
            trig = CronTrigger(hour=11, minute=29, second=0)
            # scheduler.add_job(func=begin, args=(driver,), trigger='cron', hour=11, minute=29, second=0)
        else:
            # test
            trig = CronTrigger(minute=testMin, second=0)
            # scheduler.add_job(func=begin, args=(driver,), trigger='cron', minute=testMin, second=0)
        # scheduler.add_job(func=begin, args=(driver,), trigger='cron', minute=29, second='0')
        scheduler.add_job(func=begin, args=(driver,), trigger=trig)
        scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        scheduler._logger = logging
        scheduler.start()
    except Exception:
        traceback.print_exc()
    finally:
        logging.info('程序结束')
        quit()


def begin(driver):
    print('start')
    logging.info('start, ifForceBid: ' + str(ifForceBid) + ', ifSavePrice: ' + str(ifSavePrice))
    start_time = time.time()
    error_count = 0
    threads = []

    global infoDir, webDir
    element = driver.find_element_by_id('testsocket')
    infoDir['left'] = element.location['x'] + int(infoLeft)
    infoDir['top'] = element.location['y'] + int(infoTop)
    infoDir['right'] = element.location['x'] + int(infoRight)
    infoDir['bottom'] = element.location['y'] + int(infoBottom)
    webDir['left'] = element.location['x']
    webDir['top'] = element.location['y']
    webDir['right'] = element.location['x'] + element.size['width']
    webDir['bottom'] = element.location['y'] + element.size['height']

    while time.time() - start_time <= 90:
        start_sec = time.time()
        now1 = time.strftime('%Y%m%d%H%M%S', time.localtime())
        now2 = time.strftime('%H:%M:%S', time.localtime())

        if ifSavePrice:
            price_file_name = 'resource/screen/price_' + now1 + '.png'
            global curPrice
            with lock:
                # 当前价截图
                now = time.time()
                img = driver.get_screenshot_as_png()
                if time.time() - now > 2:
                    logging.warning('请切回ie页面')
            img = Image.open(BytesIO(img))
            img = img.crop((infoDir['left'], infoDir['top'], infoDir['right'], infoDir['bottom']))
            img.save(price_file_name)

            # ocr
            base_str = baidu_ocr.img_to_str(price_file_name)
            if base_str is None:
                error_count += 1
                continue
            for i in range(len(base_str)):
                s = base_str[i]['words']
                if '目前最低可成交价' in s:
                    curPrice = s.split(':')[1]
                    if curPrice.strip() == '':
                        logging.warning('价格识别分段')
                        try:
                            curPrice = base_str[i + 1]['words']
                        except Exception:
                            error_count += 1
                            logging.error('价格识别分段识别出错')
                            # print('价格识别分段识别出错')
                            break
                    if not curPrice.isdigit():
                        logging.debug(now2 + ': 识别的字符串为: ' + curPrice)
                        # print(now2 + ': 识别的字符串为: ' + curPrice)
                        curPrice = re.sub('\D', '', curPrice)

                    length = 5
                    while len(curPrice) < length:
                        logging.debug(now2 + ' before: ' + curPrice)
                        curPrice += '0'
                        length -= 1

                    logging.info(now2 + ': ' + curPrice)
                    # print(now2 + ': ' + curPrice)
                    break

        # 判定是否到达出价时间
        thread2 = None
        thread3 = None
        if now2[6:] == secondSec:
            # 到出价时间，出价
            thread2 = threading.Thread(target=bid_thread, args=(int(curPrice) + int(secondPrice), driver, '第二次'))
            thread2.start()
            threads.append(thread2)
        elif thirdPrice != 0 and now2[6:] == thirdSec:
            thread3 = threading.Thread(target=bid_thread, args=(int(curPrice) + int(secondPrice), driver, '第三次'))
            thread3.start()
            threads.append(thread3)

        s = time.time() - start_sec
        while s < 0:
            s += 1
        if s < 1:
            time.sleep(1 - s)
        else:
            logging.info('判断超时：' + str(s))

    for thread in threads:
        thread.join()

    while True:
        pass


def bid_thread(price, driver, name):
    logging.info('启动' + name + '出价线程')
    with thread_lock:
        bid(price, driver)
        time.sleep(50)


def bid(price, driver):
    if ifForceBid:
        force_time = int(time.time() - time.localtime()[5]) + forceBidMillis
    else:
        force_time = sys.maxsize
    # 输入价格，点击出价按钮
    with lock:
        actions = ActionChains(driver)
        now = time.time()
        element = driver.find_element_by_id('testsocket')
        if ifSavePrice:
            actions.move_to_element_with_offset(element, priceX, priceY).click().send_keys(price)
        else:
            actions.move_to_element_with_offset(element, pricePlusX, pricePlusY).click().send_keys(price)
            actions.move_to_element_with_offset(element, pricePlusEnterX, pricePlusEnterY).click()
        actions.move_to_element_with_offset(element, bidX, bidY).click()
        # 弹出验证码，光标定位到输入框
        actions.move_to_element_with_offset(element, yzmEnterX, yzmEnterY).click()
        actions.perform()

    # 验证码刷新

    logging.info('出价时间: ' + str(time.time() - now) + 's')

    # 识别确定按钮位置
    time.sleep(0.5)
    file_name = 'resource/screen/now_confirm.png'
    with lock:
        img = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img))
    img = img.crop((webDir['left'], webDir['top'], webDir['right'], webDir['bottom']))
    img.save(file_name)
    confirmX, confirmY = opencv_util.find_image_cv('resource/button/confirm.png', file_name)
    logging.info('confirm located: ' + str(confirmX) + ', ' + str(confirmY))

    # 输入验证码，监听回车键
    now = time.time()
    with keyboard.Listener(on_press=press) as listener:
        listener.join()
    logging.info('输入验证码时间：' + str(time.time() - now) + 's')

    # 判断是否在出价区间或到强制提交时间，在则提交
    if ifSavePrice:
        while int(curPrice) + 300 < price and time.time() < force_time - 0.4:
            logging.info('当前价为：' + curPrice + '，' + str(price) + '不在出价区间，强制提交时间：' +
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(force_time)))
            time.sleep(0.1)
    else:
        while time.time() < force_time - 0.4:
            logging.info('当前价为：' + curPrice + '，' + str(price) + '不在出价区间，强制提交时间：' +
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(force_time)))
            time.sleep(0.1)
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '出价，加价/价格为' + str(price) + '元')
    # while (int(diff) != 0 and int(curPrice) - diff < price) and (int(liePrice) != 0 and int(curPrice) < int(liePrice)):
    #     print('当前价为：' + curPrice + '，未到埋伏价' + liePrice)
    #     time.sleep(0.1)

    with lock:
        now = time.time()
        actions2 = ActionChains(driver)
        actions2.move_to_element_with_offset(element, confirmX, confirmY).click().perform()
    logging.info('提交时延: ' + str(time.time() - now) + 's')
    listener.stop()


def my_listener(event):
    if event.exception:
        print(event.exception)


def press(key):
    if key == keyboard.Key.enter:
        return False


if __name__ == '__main__':
    pp()
