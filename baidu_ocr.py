import re

from aip import AipOcr
import time
import logging
import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log/log-' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d') + '.txt',
                    filemode='a')

config = {
    'appId': '15808024',
    'apiKey': 'OGAfuGVnLtUrBB9VF8mENGoe',
    'secretKey': 'eXcUXguSlGZx6kG7Il2inpNEBESNOfxG'
}

client = AipOcr(**config)
client.setConnectionTimeoutInMillis(1000)
client.setSocketTimeoutInMillis(500)


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    if 'error_code' in result:
        logging.warning(result)
        # time.sleep(0.1)
        result = client.basicGeneral(image)
        if 'error_code' in result:
            logging.error(result)
            return None
    return result['words_result']
    # if 'words_result' in result:
    #     return '\n'.join([w['words'] for w in result['words_result']])


def test(base_str):
    now2 = time.strftime('%H:%M:%S', time.localtime())
    for i in range(len(base_str)):
        s = base_str[i]['words']
        if '目前最低可成交价' in s:
            curPrice = s.split(':')[1]
            if curPrice.strip() == '':
                logging.warning('价格识别分段')
                try:
                    curPrice = base_str[i + 1]['words']
                except Exception:
                    logging.error('价格识别分段识别出错')
                    print('价格识别分段识别出错')
                    break
            if not curPrice.isdigit():
                print(now2 + ': 识别的字符串为: ' + curPrice)
                curPrice = re.sub('\D', '', curPrice)

            length = 5
            while len(curPrice) < length:
                logging.debug(now2 + ' before: ' + curPrice)
                curPrice += '0'
                length -= 1

            logging.info(now2 + ': ' + curPrice)
            print(now2 + ': ' + curPrice)
            break


if __name__ == '__main__':
    now = time.time()
    print(img_to_str('resource/screen/1.png'))
    diff = time.time() - now
    print(diff)

    now = time.time()
    print(img_to_str('resource/screen/2.png'))
    diff = time.time() - now
    print(diff)
    test(img_to_str('resource/screen/2.png'))

    now = time.time()
    print(img_to_str('resource/screen/3.png'))
    diff = time.time() - now
    print(diff)
    test(img_to_str('resource/screen/3.png'))

    now = time.time()
    print(img_to_str(r'C:\Workspaces\python\pp\resource\screen\price_20190614105758.png'))
    diff = time.time() - now
    print(diff)
