
import sys


from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QLineEdit, QApplication, QTextEdit, QLabel


class Patient_Dash_Board(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Dashboard")
        Layout = QGridLayout(self)
        self.setLayout(Layout)

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

        previous_history_label = QLabel(self)
        previous_history_label.setText("Previous History")
        Layout.addWidget(previous_history_label,2,1)

        previous_history_edit = QTextEdit(self)
        previous_history_edit.setReadOnly(True)
        Layout.addWidget(previous_history_edit, 3, 1,6,10)

        today_history_label = QLabel(self);
        today_history_label.setText("Today History")
        Layout.addWidget(today_history_label, 9, 1)
        today_history_edit = QTextEdit(self)
        today_history_edit.setReadOnly(False)
        Layout.addWidget(today_history_edit, 10, 1, 6, 10)

        today_examination_label = QLabel(self);
        today_examination_label.setText("Today Examination")
        Layout.addWidget(today_examination_label, 19, 1)
        today_examination_edit = QTextEdit(self)
        today_examination_edit.setReadOnly(False)
        Layout.addWidget(today_examination_edit, 20, 1, 6, 10)

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