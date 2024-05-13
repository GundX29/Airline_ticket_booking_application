from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QLineEdit, QDialogButtonBox, \
                            QFormLayout, QMessageBox, QVBoxLayout, QListWidgetItem ,QLabel, QHBoxLayout
from PyQt6 import uic
import sys
import json
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton
import requests
from Admin import admin
from Chuc_nang_json import AnimeDatabase
import smtplib
import random
from email.mime.text import MIMEText
otp = ''.join(random.choice('0123456789') for _ in range(6))

##Data user and password
Data_user = []
Data_password = []


#Code trang login
class login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/login.ui",self)
        self.show()

        self.btnLogin.clicked.connect(self.check_login)
        self.btnLogin.clicked.connect(self.send_OTP)
        self.btn_register.clicked.connect(self.show_register)

    def check_login(self):
        """Lấy thông tin email và mật khẩu từ người dùng"""
        global email_login
        email_login = self.txtEmail.text()
        password_login = self.txtPassword.text()

        if email_login == "dungpham29803@gmail.com" and password_login == "admin":
            r_admin.show()
            self.close()

        elif not email_login:
            QMessageBox.information(self, "Error","Vui lòng nhập email hoặc số điện thoại!")
            return
        elif not password_login:
            QMessageBox.information(self, "Error","Vui lòng nhập mật khẩu!")
            return
        
        elif email_login in Data_user and password_login in Data_password and Data_user.index(email_login) == Data_password.index(password_login) :
            QMessageBox.information(self ,"Check", "The OTP code has been sent to your email. Please check and confirm")
            r_checkOTP.show()            
            self.close()
        else:
            QMessageBox.information(self, "Error","Email hoặc mật khẩu không đúng!")
    
    def send_OTP(self):
        email = "dungxxx29803@gmail.com"
        passw = "trga klii ghgz yjku"
        email_sent = email_login
        print(otp)
        ##
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls() ## Bật cái bảo mật của gmail lên
        session.login(email, passw)

        ## Nội dung gửi mail
        mail_content = f'''Subject: Mã OTP để đăng nhập của bạn
        {otp}
        '''

        # Tạo đối tượng MIMEText để chứa nội dung email
        message = MIMEText(mail_content)
        message["Subject"] = "Mã OTP để đăng nhập"
        message["From"] = email
        message["To"] = email_sent

        session.sendmail(email, email_sent, message.as_string())
        print("mail sent")

    def show_register(self):
        r_resgister.show()
        self.close()
    

#Lớp chứa giao diện đăng ký
class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/register.ui", self)
        

        """ Bắt sự kiện click chuột vào nút đăng ký"""
        self.btnRegister.clicked.connect(self.register)
        self.btn_Login.clicked.connect(self.show_login)

    def register(self):
        """Lấy thông tin email, username và mật khẩu từ người dùng"""
        name_register = self.txtUsername.text()
        email_register = self.txtEmail.text()
        Data_user.append(email_register)
        password_register = self.txtPassword.text()
        Data_password.append(password_register)
        print(Data_user, Data_password)

        """ Kiểm tra các trường thông tin có được nhập hay không"""
        if not name_register:
            QMessageBox.information(self, "Error","Vui lòng nhập username!")
            return
        if not email_register:
            QMessageBox.information(self, "Error","Vui lòng nhập email hoặc số điện thoại!")
            return
        if not password_register:
            QMessageBox.information(self, "Error","Vui lòng nhập mật khẩu!")
            return
        if not self.checkBox.isChecked():
            QMessageBox.information(self, "Error","Vui lòng đọc và đồng ý các điều khoản của MemberHub!")
            return

    def show_login(self):
        r_login.show()
        self.close()


class check_OTP(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/check_OTP.ui",self)
        self.btn_checkOTP.clicked.connect(self.check_yourOTP)
    
    def check_yourOTP(self):
        your_OTP = self.btn_OTP.text()
        if your_OTP == otp:
            QMessageBox.information(self,"Valid", "Successful login")
            r_main.show()
            self.close()

class ticket_user(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        global widgets_user
        widgets_user = uic.loadUi(r"D:\BTL-Python\GUI\ticket_user.ui", self)

        global database
        database = AnimeDatabase()
        self.setup_CRUD_page()


        self.dialog = DetailDialog()  # Khởi tạo dialog ở ngoài vòng lặp
        widgets_user.animeList.itemClicked.connect(self.show_details)
        with open(r"D:\BTL-Python\data_8.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

        for item in self.data:
            title = item["Name_flight"]
            list_item = QListWidgetItem(title)
            widgets_user.animeList.addItem(list_item)
        

    def show_details(self, item):
        title_clicked = item.text()
        for obj in self.data:
            if obj["Name_flight"] == title_clicked:
                Id_flight = obj["Id_flight"]
                release_date = obj["Time_start"]
                image_url = obj["image"]
                rating = obj["Time_stop"]
                self.dialog.set_data(Id_flight,release_date, rating, image_url)
                self.dialog.exec()

    def setup_CRUD_page(self):
        database.load_data()
        # widgets.animeList.addItems(database.anime_item_list)
        widgets_user.animeList.setCurrentRow(0)


class DetailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detail")
        layout = QVBoxLayout(self)
        
        self.Id_flight_label = QLabel()
        layout.addWidget(self.Id_flight_label)
        self.Time_start_label = QLabel()
        layout.addWidget(self.Time_start_label)
        self.Time_stop_label = QLabel()
        layout.addWidget(self.Time_stop_label)
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # Thêm nút "Buy" và "Cancel"
        self.buy_button = QPushButton("Buy")
        self.cancel_button = QPushButton("Cancel")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)

        self.buy_button.clicked.connect(self.buy_action)
        self.cancel_button.clicked.connect(self.cancel_action)

    def set_data(self, Id_flight, release_date, rating, image_url):
        self.Id_flight_label.setText(f"Id_flight: {Id_flight}")
        self.Time_start_label.setText(f"Time_start: {release_date}")
        self.Time_stop_label.setText(f"Time_stop: {rating}")
        response = requests.get(image_url)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(pixmap)


    def buy_action(self):
        # Thực hiện hành động mua hàng
        global email_login
        self.send_OTP_buy(email_login)
        QMessageBox.information(self, "Information", "Sending OTP for purchase verification.")
        

    def cancel_action(self):
        # Thực hiện hành động hủy
        self.close()
    
    def send_OTP_buy(self, email_login):
        otp_purchase = ''.join(random.choice('0123456789') for _ in range(6))
        email = "dungxxx29803@gmail.com"
        passw = "trga klii ghgz yjku"
        email_sent = email_login
        print(otp_purchase)
        ##
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls() ## Bật cái bảo mật của gmail lên
        session.login(email, passw)

        ## Nội dung gửi mail
        mail_content = f'''Subject: Mã OTP để xác nhận vé của bạn
        {otp_purchase}
        '''

        # Tạo đối tượng MIMEText để chứa nội dung email
        message = MIMEText(mail_content)
        message["Subject"] = "Mã OTP để xác minh vé"
        message["From"] = email
        message["To"] = email_sent

        session.sendmail(email, email_sent, message.as_string())
        print("mail sent")

    def show_register(self):
        r_resgister.show()
        self.close()
    
        
class main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/main.ui",self)
        # self.show()

        self.bt_info.clicked.connect(self.show_info)
        self.bt_setting.clicked.connect(self.show_setting)
        self.bt_notion.clicked.connect(self.show_notion)
        self.bt_location.clicked.connect(self.show_location)
        self.bt_hotel.clicked.connect(self.show_hotel)
        self.bt_car.clicked.connect(self.show_car)
        self.bt_search.clicked.connect(self.show_search_ticket)

    def show_search_ticket(self):
        r_ticket_search.show()
        self.close()

    def show_setting(self):
        r_notFound.show()
        self.close()

    def show_notion(self):
        r_notFound.show()
        self.close()
        
    def show_info(self):
        r_user_info.show()
        self.close()

    def show_location(self):
        r_notFound.show()
        self.close()
    
    def show_hotel(self):
        r_notFound.show()
        self.close()

    def show_car(self):
        r_notFound.show()
        self.close()

    def buy_ticket(self):
        global email_login
        email_login = "example@example.com"  # Set email_login to the email of the logged-in user
        self.dialog.buy_action(email_login)  # Pass email_login to the buy_action function

    def create_ticket_dialog(self):
        self.dialog = DetailDialog()
        self.dialog.exec()
    

class notFound(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/notFound.ui", self)

        self.bt_back.clicked.connect(self.return_home)
    
    def return_home(self):
        self.close()
        r_main.show()


class user_info(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/user_info.ui", self)
        self.bt_back.clicked.connect(self.return_home)
        self.bt_log_out.clicked.connect(self.log_out)

    def return_home(self):
        self.close()
        r_main.show()

    def log_out(self):
        r_login.show()
        self.close()


app = QApplication(sys.argv)
r_login = login()
r_admin = admin()
r_ticket_search = ticket_user()
r_resgister = Register()
r_checkOTP = check_OTP()
r_main = main()
r_user_info = user_info()
r_notFound = notFound()
app.exec()