
import sys


from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QLineEdit, QApplication, QTextEdit, \
    QLabel, QRadioButton


class PatientDashBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Dashboard")


        quadrant_width=640
        quadrant_height=490

        def set_quadrants_size(widget, width=450, height=450):
            widget.setMaximumWidth(width)
            widget.setMaximumHeight(height)
            widget.setMinimumHeight(height)
            widget.setMinimumWidth(width)

        ##############################################################################
        #setting main lay out that will contain 4 Qgridlayouts each for each quadrant#
        ##############################################################################
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        self.move(0, 0)

        ######################################################################
        #setting up the ULQ which is the patient old history and demographics#
        ######################################################################
        patient_demo_and_old_data_widget=QWidget(self)
        patient_demo_and_old_data_layout = QGridLayout(patient_demo_and_old_data_widget)
        patient_demo_and_old_data_widget.setLayout(patient_demo_and_old_data_layout)
        set_quadrants_size(patient_demo_and_old_data_widget,quadrant_width,quadrant_height)


        patient_name_edit = QLineEdit(self)
        patient_name_edit.setPlaceholderText("Patient Name")
        patient_demo_and_old_data_layout.addWidget(patient_name_edit,1,1)
        # create patient_... variable and assign text to it
        patient_name_edit.textChanged.connect(lambda text: setattr(self,"patient_name",text))

        patient_DOB_edit = QLineEdit(self)
        patient_DOB_edit.setPlaceholderText("DOB")
        patient_demo_and_old_data_layout.addWidget(patient_DOB_edit, 1, 2)
        # create patient_... variable and assign text to it
        patient_DOB_edit.textChanged.connect(lambda text: setattr(self, "patient_DOB", int(text)))

        patient_residence_edit = QLineEdit(self)
        patient_residence_edit.setPlaceholderText("ٌResidence")
        patient_demo_and_old_data_layout.addWidget(patient_residence_edit, 1, 3)
        # create patient_... variable and assign text to it
        patient_residence_edit.textChanged.connect(lambda text: setattr(self, "patient_residence", text))

        #previous history
        # label
        previous_history_label = QLabel(self)
        previous_history_label.setText("Previous History")
        patient_demo_and_old_data_layout.addWidget(previous_history_label,2,1)

        # previous history
        # text edit
        previous_history_edit = QTextEdit(self)
        previous_history_edit.setReadOnly(True)
        patient_demo_and_old_data_layout.addWidget(previous_history_edit, 3, 1,1,3)

        main_layout.addWidget(patient_demo_and_old_data_widget,1,1)

        ##########################################################################
        # setting up the LLQ which is the patient current history and examination#
        ##########################################################################

        patient_today_clinical_widget=QWidget(self)
        patient_today_clinical_layout = QGridLayout(patient_today_clinical_widget)
        patient_today_clinical_widget.setLayout(patient_today_clinical_layout)
        set_quadrants_size(patient_today_clinical_widget,quadrant_width,quadrant_height)

        #Today history
        #label
        today_history_label = QLabel(self);
        today_history_label.setText("Today History")
        patient_today_clinical_layout.addWidget(today_history_label, 1, 1)

        # Today history
        #text Edit
        today_history_edit = QTextEdit(self)
        today_history_edit.setReadOnly(False)
        patient_today_clinical_layout.addWidget(today_history_edit, 2, 1, 1, 1)

        #Today Examination
        #label
        today_examination_label = QLabel(self);
        today_examination_label.setText("Today Examination")
        patient_today_clinical_layout.addWidget(today_examination_label, 1, 2)

        # Today Examination
        #text edit
        today_examination_edit = QTextEdit(self)
        today_examination_edit.setReadOnly(False)
        patient_today_clinical_layout.addWidget(today_examination_edit, 2, 2, 1 ,1)

        main_layout.addWidget(patient_today_clinical_widget,2,1)

        ##########################################################################
        # setting up the RUQ which is the patient current history and examination#
        ##########################################################################

        patient_today_ix_medication_widget=QWidget(self)
        patient_today_ix_medication_layout = QGridLayout(patient_today_ix_medication_widget)
        patient_today_ix_medication_widget.setLayout(patient_today_ix_medication_layout)
        set_quadrants_size(patient_today_ix_medication_widget,quadrant_width,quadrant_height)

        # today investigations
        # label
        today_investigations_label = QLabel(self)
        today_investigations_label.setText("Today Investigations")
        patient_today_ix_medication_layout.addWidget(today_investigations_label, 1, 1)

        # today investigations
        # text edit
        today_investigations_edit = QTextEdit(self)
        today_investigations_edit.setReadOnly(False)
        patient_today_ix_medication_layout.addWidget(today_investigations_edit, 2, 1, 1, 1)

        # Last medications == today modeications
        # label
        last_medications_label = QLabel(self)
        last_medications_label.setText("Today Medications")
        patient_today_ix_medication_layout.addWidget(last_medications_label, 1, 2)

        # today medications
        # text edit
        last_medications_edit = QTextEdit(self)
        last_medications_edit.setReadOnly(False)
        patient_today_ix_medication_layout.addWidget(last_medications_edit, 2, 2, 1, 1)

        # today investigation intelligent
        # line edit
        today_investigations_line = QLineEdit(self)
        today_investigations_line.setPlaceholderText("Intelligent Fill")
        today_investigations_line.setReadOnly(False)
        patient_today_ix_medication_layout.addWidget(today_investigations_line, 3, 1, 1, 1)

        # today Medication intelligent
        # line edit
        today_medication_line = QLineEdit(self)
        today_medication_line.setPlaceholderText("Intelligent Fill")
        today_medication_line.setReadOnly(False)
        patient_today_ix_medication_layout.addWidget(today_medication_line, 3, 2, 1, 1)

        main_layout.addWidget(patient_today_ix_medication_widget,1,2)

    #Just Button
        # fetch_path_button = QPushButton(self)
        # fetch_path_button.setText("Fetch Path")
        # Layout.addWidget(fetch_path_button, 30, 1)
        # fetch_path_button.clicked.connect(self.open_path_dialog)
        # main_layout.addWidget(patient_demo_and_old_data_widget)
        #


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
    window = PatientDashBoard()
    window.show()
    app.exec()