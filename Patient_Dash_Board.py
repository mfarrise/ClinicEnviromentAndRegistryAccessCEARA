
import sys


from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QLineEdit, QApplication, QTextEdit, \
    QLabel, QRadioButton


class Patient_Dash_Board(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Dashboard")
        # self.setMaximumSize(1000, 900)
        Layout = QGridLayout(self)
        self.setLayout(Layout)
        self.move(0,0)
        ruler=QLabel(self)
        Layout.addWidget(ruler,0,0,1,140)


        patient_name_edit = QLineEdit(self)
        patient_name_edit.setPlaceholderText("Patient Name")
        Layout.addWidget(patient_name_edit,1,1)
        # create patient_... variable and assign text to it
        patient_name_edit.textChanged.connect(lambda text: setattr(self,"patient_name",text))

        patient_DOB_edit = QLineEdit(self)
        patient_DOB_edit.setPlaceholderText("DOB")
        Layout.addWidget(patient_DOB_edit, 1, 2)
        # create patient_... variable and assign text to it
        patient_DOB_edit.textChanged.connect(lambda text: setattr(self, "patient_DOB", int(text)))

        patient_residence_edit = QLineEdit(self)
        patient_residence_edit.setPlaceholderText("ٌResidence")
        Layout.addWidget(patient_residence_edit, 1, 3)
        # create patient_... variable and assign text to it
        patient_residence_edit.textChanged.connect(lambda text: setattr(self, "patient_residence", text))

        #previous history
        # label
        previous_history_label = QLabel(self)
        previous_history_label.setText("Previous History")
        Layout.addWidget(previous_history_label,2,1)

        # previous history
        # text edit
        previous_history_edit = QTextEdit(self)
        previous_history_edit.setReadOnly(True)
        Layout.addWidget(previous_history_edit, 3, 1,30,20)

        # Last investigations
        # label
        last_investigations_label = QLabel(self)
        last_investigations_label.setText("last investigations")
        Layout.addWidget(last_investigations_label, 33, 1)

        # last_investigations
        # text edit
        last_investigations_edit = QTextEdit(self)
        last_investigations_edit.setReadOnly(True)
        Layout.addWidget(last_investigations_edit, 34, 1, 30, 2)

        # Last medications
        # label
        last_medications_label = QLabel(self)
        last_medications_label.setText("last medications")
        Layout.addWidget(last_medications_label, 33, 4)

        # last medications
        # text edit
        last_medications_edit = QTextEdit(self)
        last_medications_edit.setReadOnly(True)
        Layout.addWidget(last_medications_edit, 34, 4, 30, 10)

        #Today history
        #label
        today_history_label = QLabel(self);
        today_history_label.setText("Today History")
        Layout.addWidget(today_history_label, 2, 21)

        # Today history
        #Line Edit
        today_history_edit = QTextEdit(self)
        today_history_edit.setReadOnly(False)
        Layout.addWidget(today_history_edit, 3, 21, 25, 21)

        #Today Examination
        #label
        today_examination_label = QLabel(self);
        today_examination_label.setText("Today Examination")
        Layout.addWidget(today_examination_label, 28, 21)

        # Today Examination
        #text edit
        today_examination_edit = QTextEdit(self)
        today_examination_edit.setReadOnly(False)
        Layout.addWidget(today_examination_edit, 29, 21, 6, 20)

    #Just Button
        fetch_path_button = QPushButton(self)
        fetch_path_button.setText("Fetch Path")
        Layout.addWidget(fetch_path_button, 30, 1)
        fetch_path_button.clicked.connect(self.open_path_dialog)


    def open_path_dialog(self):
        print(self.patient_residence)
        file_path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Select file",
            dir="",
            filter="All Files (*.*);;Word Files (*.docx);;PDF Files (*.pdf)"
        )




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Patient_Dash_Board()
    window.show()
    app.exec()