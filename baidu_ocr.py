import json

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
    'appId': '',
    'apiKey': '',
    'secretKey': ''
}

client = AipOcr(**config)
client.setConnectionTimeoutInMillis(1000)
client.setSocketTimeoutInMillis(500)


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    st = time.time()
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    et = time.time()
    logging.info('ocr request: ' + str(et - st) + 's, result: ' + json.dumps(result))
    if 'error_code' in result:
        logging.warning(result)
        result = client.basicGeneral(image)
        if 'error_code' in result:
            logging.error('baidu ocr error: ' + result)
            return None
    return result['words_result']


if __name__ == '__main__':
    now = time.time()
    print(img_to_str('resource/screen/1.png'))
    diff = time.time() - now
    print(diff)

    now = time.time()
    print(img_to_str('resource/screen/2.png'))
    diff = time.time() - now
    print(diff)
