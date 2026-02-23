import sys
from datetime import datetime
from PySide6.QtCore import Qt, QLocale
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QLineEdit, QPushButton, QSizePolicy, QComboBox
from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QBrush, QIntValidator, QDoubleValidator


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

        self.date_label = QLabel("Date")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.date_label, 0, 0)

        self.date_edit = QDateEdit()
        self.date_edit.setFocusPolicy(Qt.ClickFocus)
        self.date_edit.setCalendarPopup(True)
        # Force English locale
        self.date_edit.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        # ISO display format
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        # Default to today
        self.date_edit.setDate(QDate.currentDate())
        calendar = self.date_edit.calendarWidget()
        #reseting the colour of all days to get rid from red font for sat and sunday
        default_format = QTextCharFormat()
        for day in range(1, 8):  # Qt weekday numbers 1=Mon ... 7=Sun
            calendar.setWeekdayTextFormat(Qt.DayOfWeek(day), default_format)
        #now recolor thursday and friday red
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QBrush(Qt.red))  # or Qt.gray if you prefer subtle
        calendar.setWeekdayTextFormat(Qt.Thursday, weekend_format)
        calendar.setWeekdayTextFormat(Qt.Friday, weekend_format)
        self.data_input_layout.addWidget(self.date_edit, 1,0)

        self.patients_no_label = QLabel("Patients No.")
        self.patients_no_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.patients_no_label, 0, 1)

        self.p_no_line_edit = QLineEdit()
        self.p_no_line_edit.setPlaceholderText("insert number")
        self.p_no_line_edit.setValidator(QIntValidator(0, 100))
        self.p_no_line_edit.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.p_no_line_edit, 1, 1)

        self.amount_label = QLabel("Amount")
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.amount_label, 0, 2)

        self.amount_line_edit = QLineEdit()
        self.amount_line_edit.setPlaceholderText("insert amount")
        self.amount_line_edit.setAlignment(Qt.AlignCenter)
        self.amount_line_edit.setValidator(
            QDoubleValidator(0.0, 1_000_000.0, 2).setLocale(QLocale.English))
        self.data_input_layout.addWidget(self.amount_line_edit, 1, 2)

        self.type_label = QLabel("Type")
        self.type_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.type_label, 0, 3)

        self.type_combo=QComboBox()
        self.type_combo.addItems(["income","expense"])
        self.data_input_layout.addWidget(self.type_combo, 1, 3)

        self.category_label = QLabel("Category")
        self.category_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.category_label, 0, 4)

        self.category_combo=QComboBox()
        self.category_combo.addItems(["visit","staff","cleaning","rent","shopping",
                                      "equipment","furniture","tax","other"])
        self.data_input_layout.addWidget(self.category_combo, 1, 4)

        self.method_label = QLabel("Method")
        self.method_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.method_label, 0, 5)

        self.method_combo=QComboBox()
        self.method_combo.addItems(["cash","transfer"])
        self.data_input_layout.addWidget(self.method_combo, 1, 5)

        self.note_label = QLabel("Note")
        self.note_label.setAlignment(Qt.AlignCenter)
        self.data_input_layout.addWidget(self.note_label, 0, 6)

        self.note_line_edit = QLineEdit()
        self.note_line_edit.setPlaceholderText("Free Note")
        self.data_input_layout.addWidget(self.note_line_edit, 1, 6)


        self.all_date_today_button = QPushButton("Today")
        self.all_date_today_button.setFocusPolicy(Qt.ClickFocus)
        self.data_input_layout.addWidget(self.all_date_today_button, 4, 2,1,3)
        self.all_date_today_button.clicked.connect(self.set_date_today)

        self.all_push_button = QPushButton("Push")
        self.data_input_layout.addWidget(self.all_push_button, 5, 2,1,3)
        # self.all_push_button.clicked.connect()



        self.finances_layout.addWidget(self.data_input_section,0,0)#change position later when other sublayout are added
        self.data_input_section.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )
        #endregion


    def set_date_today(self):
        self.date_edit.setDate(QDate.currentDate())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Finances()
    window.show()
    sys.exit(app.exec())
