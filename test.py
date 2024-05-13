from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import sys


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/main.ui",self)
        self.show()

        self.bt_info.clicked.connect(self.show_info)
        self.bt_setting.clicked.connect(self.show_setting)
        self.bt_notion.clicked.connect(self.show_notion)

    def show_setting(self):
        r_notFound.show()
        self.close()

    def show_notion(self):
        r_notFound.show()
        self.close()

    def show_info(self):
        r_user_info.show()
        self.close()

class notFound(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/notFound.ui", self)

class user_info(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/user_info.ui", self)
        self.bt_back.clicked.connect(self.return_home)

    def return_home(self):
        self.close()
        r_main.show()


app = QApplication(sys.argv)
r_main = main()
r_user_info = user_info()
r_notFound = notFound()
app.exec()