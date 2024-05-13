import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QLineEdit, QDialogButtonBox, \
                            QFormLayout, QMessageBox, QVBoxLayout, QListWidgetItem ,QLabel
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from Chuc_nang_json import AnimeDatabase
import requests
import json


class admin(QMainWindow):
    def __init__(self):
        super().__init__()
        global widgets
        widgets = uic.loadUi(r"D:\BTL-Python\GUI\CRUD.ui", self)

        global database
        database = AnimeDatabase()
        self.setup_CRUD_page()


        self.dialog = DetailDialog()  # Khởi tạo dialog ở ngoài vòng lặp
        widgets.animeList.itemClicked.connect(self.show_details)
        with open(r"D:\BTL-Python\data_8.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

        for item in self.data:
            title = item["Name_flight"]
            list_item = QListWidgetItem(title)
            widgets.animeList.addItem(list_item)
        

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
        widgets.animeList.setCurrentRow(0)
        widgets.addButton.clicked.connect(lambda:AnimeCRUD.add(self))
        widgets.removeButton.clicked.connect(lambda:AnimeCRUD.delete(self))
        widgets.editButton.clicked.connect(lambda:AnimeCRUD.edit(self))

class AnimeCRUD():
    def add(self):
        currIndex = widgets.animeList.currentRow()
        add_dialog = AddDialog()
        if add_dialog.exec():
            inputs = add_dialog.getInputs()
            widgets.animeList.insertItem(currIndex, inputs["Name_flight"])
            database.add_item_from_dict(inputs)

    def edit(self):
        currIndex = widgets.animeList.currentRow()
        item = widgets.animeList.item(currIndex)
        if item is not None:  # Kiểm tra xem mục có tồn tại không
            item_title = item.text()
            anime_item = database.get_item_by_title(item_title)
            edit_dialog = EditDialog(anime_item)
            if edit_dialog.exec():
                inputs = edit_dialog.getInputs()
                item.setText(inputs["Name_flight"])
                database.edit_item_from_dict(item_title, inputs)
                database.load_data()


    def delete(self):
        currIndex = widgets.animeList.currentRow()
        item = widgets.animeList.item(currIndex)
        item_title = item.text()
        if item is None:
            return
        question = QMessageBox.question(self, "Remove ticket?",
                                        "Do you want to remove this ticket?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if question == QMessageBox.StandardButton.Yes:
            item = widgets.animeList.takeItem(currIndex)
            database.delete_item(item_title)


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.Id_flight = QLineEdit(self)
        self.Name_flight = QLineEdit(self)
        self.Time_start = QLineEdit(self)
        self.image = QLineEdit(self)
        self.Time_stop = QLineEdit(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Id flight", self.Id_flight)
        layout.addRow("Name flight", self.Name_flight)
        layout.addRow("Time start", self.Time_start)
        layout.addRow("Image", self.image)
        layout.addRow("Time stop", self.Time_stop)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return {
            "Id_flight": self.Id_flight.text(),
            "Name_flight": self.Name_flight.text(),
            "Time_start": self.Time_start.text(),
            "image": self.image.text(), 
            "Time_stop": self.Time_stop.text()
        }

class DetailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detail")
        layout = QVBoxLayout(self)
        self.Id_flight_label= QLabel()
        layout.addWidget(self.Id_flight_label)
        self.Time_start_label = QLabel()
        layout.addWidget(self.Time_start_label)
        self.Time_stop_label = QLabel()
        layout.addWidget(self.Time_stop_label)
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

    def set_data(self,Id_flight, release_date, rating, image_url):
        self.Id_flight_label.setText(f"Id_flight: {Id_flight}")
        self.Time_start_label.setText(f"Time_start: {release_date}")
        self.Time_stop_label.setText(f"Time_stop: {rating}")
        response = requests.get(image_url)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(pixmap)

class EditDialog(QDialog):
    def __init__(self, anime_item):
        super().__init__() 

        self.Id_flight = QLineEdit(self)
        self.Name_flight = QLineEdit()
        self.Time_start = QLineEdit(self)
        self.image = QLineEdit(self)
        self.Time_stop = QLineEdit(self)

        self.Id_flight.setText(anime_item.Id_flight)
        self.Name_flight.setText(anime_item.Name_flight)
        self.Time_start.setText(anime_item.Time_start) 
        self.image.setText(anime_item.image)
        self.Time_stop.setText(anime_item.Time_stop)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Id_flight", self.Id_flight)
        layout.addRow("Name_flight", self.Name_flight)
        layout.addRow("Time_start", self.Time_start)
        layout.addRow("Ticket", self.image)
        layout.addRow("Time_stop", self.Time_stop)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return {
            "Id_flight": self.Id_flight.text(),
            "Name_flight": self.Name_flight.text(),
            "Time_start": self.Time_start.text(),
            "image": self.image.text(), 
            "Time_stop": self.Time_stop.text()
        }
        

app_admin = QApplication(sys.argv)
window = admin()
window.show()
app_admin.exec()