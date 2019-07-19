import threading
from resource.ui.window import Ui_MainWindow
import start
import logging
import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log/log-' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d') + '.txt',
                    filemode='a')


class UiLogic(Ui_MainWindow):
    def __init__(self):
        super(UiLogic, self).__init__()
        self.setupUi(self)

    def confirmButtonClick(self):
        try:
            logging.info(
                'change before: second sec: ' + str(start.secondSec) + ', second price: ' + str(start.secondPrice) +
                ', third sec: ' + str(start.thirdSec) + ', third price: ' + str(start.thirdPrice) +
                ', if force bid: ' + str(start.ifForceBid) + ', force bid millis: ' + str(start.forceBidMillis))
            start.secondSec = self.secondBidTime.time().second()
            start.secondPrice = self.secondBidPrice.value()
            third_price = self.thirdBidPrice.value()
            if third_price != 0:
                start.thirdSec = self.thirdBidTime.time().second()
                start.secondPrice = third_price
            force_bid_checked = self.forceBid
            if force_bid_checked.isChecked():
                start.ifForceBid = True
                start.forceBidMillis = float(self.forceBidTime.time().toString('ss.zzz'))
            logging.info(
                'change after: second sec: ' + str(start.secondSec) + ', second price: ' + str(start.secondPrice) +
                ', third sec: ' + str(start.thirdSec) + ', third price: ' + str(start.thirdPrice) +
                ', if force bid: ' + str(start.ifForceBid) + ', force bid millis: ' + str(start.forceBidMillis))
        except Exception as e:
            logging.error('confirmButtonClick error: ', e)

    def formalPpClick(self):
        logging.info('begin formal pp')
        thread = threading.Thread(target=start.pp, args=(False,))
        thread.start()

    def testPpClick(self):
        logging.info('begin test pp')
        thread = threading.Thread(target=start.pp, args=(True,))
        thread.start()
