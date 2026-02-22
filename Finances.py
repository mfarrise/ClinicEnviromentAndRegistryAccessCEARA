import sys
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QLineEdit, QPushButton, QSizePolicy


#ill also creat sub layouts that sit inside the finances_layout for the sake of sanity of my mind
class Finances(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance")
        self.finances_layout = QGridLayout()
        self.setLayout(self.finances_layout)

        #################         data input section     ###############
        #region

        self.data_input_section=QWidget()
        self.data_input_layout = QGridLayout()
        self.data_input_section.setLayout(self.data_input_layout)

        self.date_label = QLabel("Dates")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.date_label, 0, 1)

        self.entries_label = QLabel("Entries")
        self.entries_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.entries_label, 0, 2)



        self.balance_label = QLabel("balance")
        self.data_input_layout.addWidget(self.balance_label, 1, 0)

        self.date_balance_line_edit = QLineEdit()
        self.date_balance_line_edit.setPlaceholderText("Date")
        self.date_balance_line_edit.setFocusPolicy(Qt.ClickFocus)
        self.data_input_layout.addWidget(self.date_balance_line_edit, 1, 1)

        self.balance_line_edit = QLineEdit()
        self.balance_line_edit.setPlaceholderText("insert income")
        self.data_input_layout.addWidget(self.balance_line_edit, 1, 2)

        self.balance_date_today_button = QPushButton("Today")
        self.data_input_layout.addWidget(self.balance_date_today_button, 1, 3)
        self.balance_date_today_button.setFocusPolicy(Qt.ClickFocus)
        self.balance_date_today_button.clicked.connect(self.set_date_balance)

        self.balance_push_button = QPushButton("Push")
        self.data_input_layout.addWidget(self.balance_push_button, 1, 4)
        self.balance_push_button.setFocusPolicy(Qt.ClickFocus)
        # self.balance_push_button.clicked.connect()



        self.patient_no_label = QLabel("patient No.")
        self.data_input_layout.addWidget(self.patient_no_label, 2, 0)

        self.p_no_date_line_edit = QLineEdit()
        self.p_no_date_line_edit.setPlaceholderText("Date")
        self.p_no_date_line_edit.setFocusPolicy(Qt.ClickFocus)
        self.data_input_layout.addWidget(self.p_no_date_line_edit, 2, 1)

        self.p_no_line_edit = QLineEdit()
        self.p_no_line_edit.setPlaceholderText("insert number")
        self.data_input_layout.addWidget(self.p_no_line_edit, 2, 2)

        self.p_no_date_today_button = QPushButton("Today")
        self.data_input_layout.addWidget(self.p_no_date_today_button, 2, 3)
        self.p_no_date_today_button.setFocusPolicy(Qt.ClickFocus)
        self.p_no_date_today_button.clicked.connect(self.set_date_patient_no)

        self.p_no_push_button = QPushButton("Push")
        self.data_input_layout.addWidget(self.p_no_push_button, 2, 4)
        self.p_no_push_button.setFocusPolicy(Qt.ClickFocus)
        # self.bp_no_push_button.clicked.connect()




        self.note_label = QLabel("Note")
        self.data_input_layout.addWidget(self.note_label, 3, 0)

        self.note_date_line_edit = QLineEdit()
        self.note_date_line_edit.setPlaceholderText("Date")
        self.note_date_line_edit.setFocusPolicy(Qt.ClickFocus)
        self.data_input_layout.addWidget(self.note_date_line_edit, 3, 1)

        self.note_line_edit = QLineEdit()
        self.note_line_edit.setPlaceholderText("insert note")
        self.data_input_layout.addWidget(self.note_line_edit, 3, 2)

        self.note_date_today_button = QPushButton("Today")
        self.data_input_layout.addWidget(self.note_date_today_button, 3, 3)
        self.note_date_today_button.setFocusPolicy(Qt.ClickFocus)
        self.note_date_today_button.clicked.connect(self.set_date_note)

        self.note_push_button = QPushButton("Push")
        self.data_input_layout.addWidget(self.note_push_button, 3, 4)
        self.note_push_button.setFocusPolicy(Qt.ClickFocus)
        # self.note_push_button.clicked.connect()

        self.all_date_today_button = QPushButton("Today")
        self.data_input_layout.addWidget(self.all_date_today_button, 4, 1,1,3)
        self.all_date_today_button.clicked.connect(self.set_date_all)

        self.all_push_button = QPushButton("Push")
        self.data_input_layout.addWidget(self.all_push_button, 5, 1,1,3)
        # self.all_push_button.clicked.connect()


        self.finances_layout.addWidget(self.data_input_section,0,0)#change position later when other sublayout are added
        self.data_input_section.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )
        #endregion


    def set_date_balance(self):
        self.date_balance_line_edit.setText(datetime.now().date().isoformat())
    def set_date_patient_no(self):
        self.p_no_date_line_edit.setText(datetime.now().date().isoformat())
    def set_date_note(self):
        self.note_date_line_edit.setText(datetime.now().date().isoformat())
    def set_date_all(self):
        self.set_date_balance()
        self.set_date_patient_no()
        self.set_date_note()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Finances()
    window.show()
    sys.exit(app.exec())
