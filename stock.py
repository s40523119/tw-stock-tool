import sys
from pyqtwindow import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication,QTableWidgetItem,QHeaderView,QMessageBox


#####
import requests as r
import pandas as pd
from bs4 import BeautifulSoup
#####



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.data = []
        self.isParse = False
        self.setWindowTitle("本益比法");
        self.tabledata.horizontalHeader().setStretchLastSection(True)
        self.tabledata.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



    def parseData(self,num):
        target_url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=' + str(num) + '&YEAR_PERIOD=9999&RPT_CAT=M_YEAR&STEP=DATA&SHEET=PER%2FPBR'
        headers  = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            'referer': 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2330',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        rs = r.session()
        res = rs.get(target_url, headers=headers)
        res.encoding=('utf8')
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            t = pd.read_html(res.text)
        except ValueError:
                if soup.text == '查無資料':
                    print('此股票代號查無經營績效')
                    return self.msg('incorrect-input2')
        year = list()
        high_price = list()
        low_price = list()
        avg_price = list()
        eps = list()
        for i in range(2,7):
            year.append(t[2].values[i][0])
            high_price.append(float(t[2].values[i][3]))
            low_price.append(float(t[2].values[i][4]))
            avg_price.append(float(t[2].values[i][6]))
            eps.append(float(t[2].values[i][9]))

        high_ROE = list()
        low_ROE = list()
        avg_ROE = list()

        for i in range(len(eps)):
            high_ROE.append(round(high_price[i]/eps[i], 2))
            low_ROE.append(round(low_price[i]/eps[i], 2))
            avg_ROE.append(round(avg_price[i]/eps[i], 2))

        high_price.append(round(sum(high_price) / float(len(high_price)), 2))
        low_price.append(round(sum(low_price) / float(len(low_price)), 2))
        avg_price.append(round(sum(avg_price) / float(len(avg_price)), 2))
        eps.append(round(sum(eps) / float(len(eps)), 2))
        high_ROE.append(round(sum(high_ROE) / float(len(high_ROE)), 2))
        low_ROE.append(round(sum(low_ROE) / float(len(low_ROE)), 2))
        avg_ROE.append(round(sum(avg_ROE) / float(len(avg_ROE)), 2))
        '''
        Parse 4 Season EPS
        '''
        target_url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=' + str(num) + '&YEAR_PERIOD=9999&RPT_CAT=M_QUAR_ACC'
        headers  = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            'referer': 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2330',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                }
        rs = r.session()
        res = rs.get(target_url, headers=headers)
        res.encoding=('utf8')
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            t = pd.read_html(res.text)
        except ValueError:
                if soup.text == '查無資料':
                    print('此股票代號查無經營績效')
                    return self.msg('incorrect-input2')
        recmd_EPS_list = list()
        for i in range(2,6):
                    recmd_EPS_list.append(float(t[14].values[i][-3]))
        recmd_EPS = round(sum(recmd_EPS_list) / float(len(recmd_EPS_list)), 2)
        self.lineEdit_eps.setText(str(recmd_EPS))
        self.isParse = True


        return year, high_price, low_price, avg_price, eps, high_ROE, low_ROE, avg_ROE#, recmd_EPS


    def calcData(self,gEPS):

        cheap = (self.data[-2][-1])*float(gEPS)
        good = (self.data[-1][-1])*float(gEPS)
        exp = (self.data[-3][-1])*float(gEPS)
        safe_0 = [round(cheap, 2), round(good, 2), round(exp, 2)]
        safe_5 = [round(safe_0[0]*(1-0.05), 2), round(safe_0[1]*(1-0.05), 2), round(safe_0[2]*(1-0.05), 2)]
        safe_10 = [round(safe_0[0]*(1-0.1), 2), round(safe_0[1]*(1-0.1), 2), round(safe_0[2]*(1-0.1))]
        safe_15 = [round(safe_0[0]*(1-0.15), 2), round(safe_0[1]*(1-0.15), 2), round(safe_0[2]*(1-0.15), 2)]
        safe_20 = [round(safe_0[0]*(1-0.2), 2), round(safe_0[1]*(1-0.2), 2), round(safe_0[2]*(1-0.2), 2)]
        safe_25 = [round(safe_0[0]*(1-0.25), 2), round(safe_0[1]*(1-0.25), 2), round(safe_0[2]*(1-0.25), 2)]
        safe_30 = [round(safe_0[0]*(1-0.3), 2), round(safe_0[1]*(1-0.3), 2), round(safe_0[2]*(1-0.3), 2)]


        return safe_0, safe_5, safe_10, safe_15, safe_20, safe_25, safe_30
    @pyqtSlot()
    def on_pushButton_send_clicked(self):
        '''
        Parse Data From www.goodinfo.com
        '''
        stock_num = self.lineEdit_stock_num.text()
        if stock_num == '':
            print('You Need To Enter Stock Number')
            return self.msg('no-input')
        elif len(stock_num) != 4:
            return self.msg('incorrect-input')
        elif stock_num.isdigit() == False:
            return self.msg('incorrect-input')
        else:
            self.data = self.parseData(stock_num)
            if self.isParse == True:
                for num in range(len(self.data)):
                    for i in range(len(self.data[num])):
                        item = QTableWidgetItem()
                        item.setText(str(self.data[num][i]))
                        self.tabledata.setItem(i, num, item)
                self.tabledata.repaint()
                print('Parse Done!')
    @pyqtSlot()
    def on_pushButton_calc_clicked(self):
        '''
        Calc Price
        '''
        if self.isParse:
            EPS = self.lineEdit_eps.text()
            if EPS == '':
                print('You Need To Enter EPS')
                return self.msg('no-eps')
            elif EPS.replace('.','',1).isdigit() == False:
                    return self.msg('incorrect-eps')
            else:
                safe = self.calcData(EPS)
                for num in range(0, len(safe)):
                    for i in range(len(safe[num])):
                        item = QTableWidgetItem()
                        item.setText(str(safe[num][i]))
                        self.tableprice.setItem(i, num, item)
                self.tableprice.repaint()
                print('Calc Done!')
        else:
            print('You Need To Parse Data First')
            return self.msg('no-parse')
    def msg(self,status):
        if status == 'no-input':
            reply = QMessageBox.warning(self,"警告訊息","尚未輸入股票代號!")
        elif status == 'no-parse':
            reply = QMessageBox.warning(self,"警告訊息","請先查詢股票資料，再進行計算!")
        elif status == 'no-eps':
            reply = QMessageBox.warning(self,"警告訊息","請先輸入預估EPS，再進行計算!")
        elif status == 'incorrect-input':
            reply = QMessageBox.warning(self,"警告訊息","請輸入正確股票代號，再進行查詢!")
        elif status == 'incorrect-input2':
            reply = QMessageBox.warning(self,"警告訊息","此股票代號查無經營績效!")
        elif status == 'incorrect-eps':
            reply = QMessageBox.warning(self,"警告訊息","請輸入正確EPS，再進行計算!")
        return reply



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
