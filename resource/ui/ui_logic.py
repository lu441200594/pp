import threading
from resource.ui.window import Ui_MainWindow
import main
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
                'change before: second sec: ' + str(main.secondSec) + ', second price: ' + str(main.secondPrice) +
                ', third sec: ' + str(main.thirdSec) + ', third price: ' + str(main.thirdPrice) +
                ', if force bid: ' + str(main.ifForceBid) + ', force bid millis: ' + str(main.forceBidMillis))
            main.secondSec = self.secondBidTime.time().second()
            main.secondPrice = self.secondBidPrice.value()
            third_price = self.thirdBidPrice.value()
            main.thirdSec = self.thirdBidTime.time().second()
            main.thirdPrice = third_price
            force_bid_checked = self.forceBid
            if force_bid_checked.isChecked():
                main.ifForceBid = True
                main.forceBidMillis = float(self.forceBidTime.time().toString('ss.zzz'))
            else:
                main.ifForceBid = False
            logging.info(
                'change after: second sec: ' + str(main.secondSec) + ', second price: ' + str(main.secondPrice) +
                ', third sec: ' + str(main.thirdSec) + ', third price: ' + str(main.thirdPrice) +
                ', if force bid: ' + str(main.ifForceBid) + ', force bid millis: ' + str(main.forceBidMillis))
        except Exception as e:
            logging.error('confirmButtonClick error: ', e)

    def formalPpClick(self):
        logging.info('begin formal pp')
        thread = threading.Thread(target=main.pp, args=(False,))
        thread.start()

    def testPpClick(self):
        logging.info('begin test pp')
        thread = threading.Thread(target=main.pp, args=(True,))
        thread.start()
