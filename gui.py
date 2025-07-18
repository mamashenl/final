from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(500, 30, 900, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # კატეგორიების ჩარჩო და შიგნითა კოდი
        filter_group = QtWidgets.QGroupBox(" კატეგორიების გაფილტვრა")
        filter_layout = QtWidgets.QHBoxLayout()

        self.comboBox_2 = QtWidgets.QComboBox()
        filter_layout.addWidget(QtWidgets.QLabel("აირჩიე კატეგორია:"))
        filter_layout.addWidget(self.comboBox_2)

        self.search_button = QtWidgets.QPushButton("ძებნა")
        filter_layout.addWidget(self.search_button)

        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)

        #########
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) #zgudavs editings

        header = self.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)

        main_layout.addWidget(self.tableWidget)

        # განცხადების დამატება
        entry_group = QtWidgets.QGroupBox("➕ განცხადების დამატება")
        entry_layout = QtWidgets.QGridLayout()

        self.lineEdit_4 = QtWidgets.QLineEdit()  # კატეგორია
        self.lineEdit_5 = QtWidgets.QLineEdit()  # აღწერა
        self.lineEdit_3 = QtWidgets.QLineEdit()  # თარიღი
        self.lineEdit_2 = QtWidgets.QLineEdit()  # დრო
        self.lineEdit_6 = QtWidgets.QLineEdit()  # ფასი
        self.lineEdit = QtWidgets.QLineEdit()    # პაროლი
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password) # მალავს ტექსტს

        entry_layout.addWidget(QtWidgets.QLabel("კატეგორია:"), 0, 0)
        entry_layout.addWidget(self.lineEdit_4, 0, 1)
        entry_layout.addWidget(QtWidgets.QLabel("აღწერა:"), 0, 2)
        entry_layout.addWidget(self.lineEdit_5, 0, 3)

        entry_layout.addWidget(QtWidgets.QLabel("თარიღი:"), 1, 0)
        entry_layout.addWidget(self.lineEdit_3, 1, 1)
        entry_layout.addWidget(QtWidgets.QLabel("დრო:"), 1, 2)
        entry_layout.addWidget(self.lineEdit_2, 1, 3)

        entry_layout.addWidget(QtWidgets.QLabel("ფასი:"), 2, 0)
        entry_layout.addWidget(self.lineEdit_6, 2, 1)
        entry_layout.addWidget(QtWidgets.QLabel("პაროლი:"), 2, 2)
        entry_layout.addWidget(self.lineEdit, 2, 3)

        self.pushButton = QtWidgets.QPushButton("განცხადების დამატება")
        entry_layout.addWidget(self.pushButton, 3, 3)

        entry_group.setLayout(entry_layout)
        main_layout.addWidget(entry_group)

        # ქვემოთ გამწვანებული სტატუის დამატება
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setStyleSheet("color: green; font-weight: bold;")
        main_layout.addWidget(self.label_4)

        # აახლებს კომბოქწსს
        self.comboBox_2.currentIndexChanged.connect(self.apply_filters)
        self.search_button.clicked.connect(self.apply_filters)
        self.pushButton.clicked.connect(self.insert)

        # კომბოს შევება
        self.fill_combobox(self.comboBox_2, "category")

        MainWindow.setWindowTitle("განცხადებები")

    def fill_combobox(self, combobox, column_name):
        conn = sqlite3.connect("mysql.sqlite3")
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column_name} FROM mysql")
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        values = sorted(set(values))
        combobox.clear()
        combobox.addItem("ნებისმიერი")
        combobox.addItems(values)

    def load_data_to_table(self, data):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["ყიდვა", "კატეგორია", "აღწერა", "თარიღი", "დრო", "ფასი"])

        for row_idx, row_data in enumerate(data):
            self.tableWidget.insertRow(row_idx)

            # yidva
            buy_button = QtWidgets.QPushButton("ყიდვა")
            buy_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 4px; padding: 3px;")

            # erroris amogdeba
            buy_button.clicked.connect(self.show_card_error)

            self.tableWidget.setCellWidget(row_idx, 0, buy_button)

            # დანარჩენი სვეტები
            for col_idx, value in enumerate(row_data[1:], start=1):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def show_card_error(self):
        QtWidgets.QMessageBox.warning(None, "ყიდვა", "თქვენი ბარათი არ არის მიბმული ! :))")

    def apply_filters(self):
        category = self.comboBox_2.currentText()
        query = "SELECT id, category, description, date, time, price FROM mysql WHERE 1=1"
        params = []

        if category != "ნებისმიერი":
            query += " AND category=?"
            params.append(category)

        conn = sqlite3.connect("mysql.sqlite3")
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        self.load_data_to_table(results)

    def insert(self):
        conn = sqlite3.connect("mysql.sqlite3")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM mysql")
        id = cursor.fetchone()[0]

        category = self.lineEdit_4.text()
        description = self.lineEdit_5.text()
        date = self.lineEdit_3.text()
        time = self.lineEdit_2.text()
        price = self.lineEdit_6.text()
        password = self.lineEdit.text()

        if not all([category, description, date, time, price, password]):
            self.label_4.setText(" გთხოვთ შეავსოთ ყველა ველი ,სხვაგვარად არ დაემატება")
            self.label_4.setStyleSheet("color: red; font-weight: bold;")
            return

        cursor.execute("INSERT INTO mysql VALUES (?, ?, ?, ?, ?, ?, ?)", (id, category, description, date, time, price, password))
        conn.commit()

        cursor.execute("SELECT id, category, description, date, time, price FROM mysql")
        results = cursor.fetchall()
        conn.close()

        self.load_data_to_table(results)
        self.label_4.setText(" განცხადება დაემატა ")
        self.label_4.setStyleSheet("color: green; font-weight: bold;")

        # ველების გასუფთავება
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_3.clear()
        self.lineEdit_2.clear()
        self.lineEdit_6.clear()
        self.lineEdit.clear()

        # გადავსება ახლით
        self.fill_combobox(self.comboBox_2, "category")

#პროსტაზე არ გაეშვება ან არასწორად,გვინდა რო მხოლოდ ამ შემთხვევაში შეიქმნას ეგ ფაილი
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # პაატა დიზაინი
    app.setStyleSheet("""
    QGroupBox {
        font-weight: bold;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-top: 10px;
        padding: 10px;
    }
    QPushButton {
        background-color: #0057B8;
        color: white;
        padding: 6px 12px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #003f8a;
    }
    QLineEdit, QComboBox {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    """)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # კაროჩე ეს ტვირთავს საწყისებს ცხრილში
    conn = sqlite3.connect("mysql.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, description, date, time, price FROM mysql")
    data = cursor.fetchall()
    conn.close()
    ui.load_data_to_table(data)

    MainWindow.show()
    sys.exit(app.exec_())
#done