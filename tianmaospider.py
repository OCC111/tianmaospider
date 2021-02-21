# coding=utf-8

import sys
import time
import requests
import random
from lxml import etree

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit
from PyQt5.QtGui import QTextCursor

'''
控制台输出定向到Qtextedit中
'''


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class GenMast(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.initUI()

        # Custom output stream.
        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def initUI(self):  # 初始化页面
        """Creates UI window on launch."""
        # Button for generating the master list.
        btnGenMast = QPushButton('Run', self)
        btnGenMast.move(450, 50)
        btnGenMast.resize(100, 200)
        btnGenMast.clicked.connect(self.genMastClicked)

        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(200)
        self.process.move(30, 50)

        # Set window size and title, then show the window. 设置程序左上角的标题和窗口
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('天猫Spider')
        self.setWindowIcon(QIcon('favicon.ico'))
        self.show()

    def printhello(self):

        """
        天猫爬虫模块文件主代码
        :param url:
        :return:
        """

        url = 'https://list.tmall.com/search_product.htm?q=iPhone12&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
            "Cookie": "cna=SSKhGAk3Jn4CAd6AL6cDFopf; xlly_s=1; t=f5ece71d3fba8409616804a9c9d3466b; _tb_token_=38e7db1ee664e; cookie2=1741b36d607a27641eda9945b4cae319; _med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; cq=ccp%3D1; pnm_cku822=098%23E1hvnvvUvbpvUvCkvvvvvjiWPLqWsjrmRsMZ0jYHPmPwzjEmRsLhtjDERLdh1jYRi9hvCvvv9UURvpvhvv2MMQvCvvOvCvvvphvUvpCWCUtsvvaKYWLhQCQwfCuYiXVvVE6Fp%2B0x9WpfjLEc6acEKBm6NB3rtjcQ%2BulQbfk1DfesRk9c6R2w6C0XahNp%2BneYr2E9ZRAn3w0Ahb9Cvm9vvvvvphvvvvvvvQCvpvFbvvv2vhCv2UhvvvWvphvWgvvvvQCvpvs9kvhvC99vvOCgp89Cvv9vvUmqEysyYL9Cvvpvvvvv; res=scroll%3A1519*5386-client%3A1519*754-offset%3A1519*5386-screen%3A1536*864; tfstk=cBocBA6V6qzjE0zoRnZjLXHOQlRRZ5Y4Gcor40HS2cUuH8nPiSQP8E6vEShmXN1..; l=eBPG0A4ejPn7nOPkKOfwourza77tjIRAguPzaNbMiOCP9aCHRy8NW6MZA-YMCnGVh6WMR38KdX6JBeYBqQAonxvttBALurkmn; isg=BDo6Vd-wDq9XAYJDQOrS6JAai2Bc677FsY7Y6kQz4U2TN9pxLHli1X1Fg8PrpzZd",
            "accept-encoding": "gzip, deflate, br",
        }

        self.response = requests.get(url=url, headers=headers).text

        datas = etree.HTML(self.response)

        index_data = datas.xpath('//div[@class="product-iWrap"]')

        items = {}

        # a = 0
        for list_data in index_data:
            items['title'] = list_data.xpath('.//p[@class="productTitle"]/a/@title')
            items['price'] = list_data.xpath('.//p[@class="productPrice"]/em/@title')
            items['shop'] = list_data.xpath('.//div[@class="productShop"]/a/span/text()') + list_data.xpath(
                './/div[@class="productShop"]/a/text()')

            # print(items)
            for c in items.values():
                a = random.sample(c, 1)  # 随机一个字典中的key，第二个参数为限制个数
                print(a)
            print("===========================")

    def genMastClicked(self):
        """Runs the main function."""
        print('Running...')
        self.printhello()
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()
        print('Done.')


if __name__ == '__main__':
    # Run the application.
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)

    gui = GenMast()
    gui.genMastClicked()
    gui.printhello()
    sys.exit(app.exec_())