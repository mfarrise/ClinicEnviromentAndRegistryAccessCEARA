import os
import sys
from datetime import datetime

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QLineEdit, QApplication, QTextEdit, \
    QLabel, QRadioButton, QComboBox, QMenuBar

from docx import Document

class PatientDashBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Dashboard")


        quadrant_width=540
        quadrant_height=390



        ##############################################################################
        #setting main lay out that will contain 4 Qgridlayouts each for each quadrant#
        ##############################################################################
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        self.move(0, 0)

        menu_bar=QMenuBar()
        file_menu=menu_bar.addMenu("File")
        set_directory_action=file_menu.addAction("Set Directory")
        main_layout.addWidget(menu_bar)


        ######################################################################
        #setting up the ULQ which is the patient old history and demographics#
        ######################################################################
        # region
        patient_demo_and_old_data_widget=QWidget(self)
        patient_demo_and_old_data_layout = QGridLayout(patient_demo_and_old_data_widget)
        patient_demo_and_old_data_widget.setLayout(patient_demo_and_old_data_layout)
        self.set_quadrants_size(patient_demo_and_old_data_widget,quadrant_width,quadrant_height)


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

        patient_gender_combo=QComboBox()
        patient_gender_combo.addItems(["Male","Female"])
        patient_demo_and_old_data_layout.addWidget(patient_gender_combo, 1, 4)



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
        patient_demo_and_old_data_layout.addWidget(previous_history_edit, 3, 1,1,4)

        main_layout.addWidget(patient_demo_and_old_data_widget,1,0)
        # endregion
        ##########################################################################
        # setting up the LLQ which is the patient current history and examination#
        ##########################################################################
        #region
        patient_today_clinical_widget=QWidget(self)
        patient_today_clinical_layout = QGridLayout(patient_today_clinical_widget)
        patient_today_clinical_widget.setLayout(patient_today_clinical_layout)
        self.set_quadrants_size(patient_today_clinical_widget,quadrant_width,quadrant_height)

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

        main_layout.addWidget(patient_today_clinical_widget,2,0)
        #endregion
        ##########################################################################
        # setting up the RUQ which is the patient current history and examination#
        ##########################################################################
        #region
        patient_today_ix_medication_widget=QWidget(self)
        patient_today_ix_medication_layout = QGridLayout(patient_today_ix_medication_widget)
        patient_today_ix_medication_widget.setLayout(patient_today_ix_medication_layout)
        self.set_quadrants_size(patient_today_ix_medication_widget,quadrant_width,quadrant_height)

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

        main_layout.addWidget(patient_today_ix_medication_widget,1,1)

        #endregion
        ##########################################################################
        # setting up the RUQ which is the patient current history and examination#
        ##########################################################################
        #region
        def load_patient_data():
            patient_file_path = self.open_path_dialog()

            doc = Document(patient_file_path)
            # in the following code
            # splitext() returns a tuple:
            # ("README", ".md")
            # [0]takes the first part(without extension)
            patient_name_edit.setText(os.path.splitext(os.path.basename(patient_file_path))[0])
            old_history=""
            for paragraph in doc.paragraphs:
                old_history=old_history+paragraph.text+"\n"
            previous_history_edit.setText(old_history)


        def update_patient_data():

            doc = Document()
            demographic_table=doc.add_table(2,5)

            demographic_table.cell(0,0).text="Name"
            if patient_name_edit.text() != "":
                demographic_table.cell(1,0).text=patient_name_edit.text()

            demographic_table.cell(0,1).text="DOB"
            if patient_name_edit.text() != "":
                demographic_table.cell(1,1).text=patient_DOB_edit.text()

            demographic_table.cell(0,2).text="Age"
            if patient_name_edit.text() != "":
                demographic_table.cell(1,1).text=str(datetime.now().year-int(patient_DOB_edit.text()))

            demographic_table.cell(0,3).text="Gender"
            demographic_table.cell(1,3).text=patient_gender_combo.currentText()

            demographic_table.cell(0,4).text="Residence"
            if patient_name_edit.text() != "":
                demographic_table.cell(1,4).text=patient_residence_edit.text()

            doc.save("PatientDashBoard.docx")
        io_widget=QWidget(self)
        io_layout = QGridLayout(io_widget)
        io_widget.setLayout(io_layout)
        self.set_quadrants_size(io_widget,quadrant_width,quadrant_height)

        #load patient button
        load_patient_button=QPushButton("Load Patient")
        io_layout.addWidget(load_patient_button,0,0)
        load_patient_button.clicked.connect(load_patient_data)

        #update new data button
        update_patient_button=QPushButton("Update Patient")
        io_layout.addWidget(update_patient_button,0,1)
        update_patient_button.clicked.connect(update_patient_data)



        main_layout.addWidget(io_widget,2,1)

        #endregion
        ##########################################
        #starting writing th engine of the widget#
        ##########################################









    def open_path_dialog(self):

        file_path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Select file",
            dir="",
            filter="All Files (*.*);;Word Files (*.docx);;PDF Files (*.pdf)"
        )
        #print(type(file_path),file_path)
        return file_path

    def set_quadrants_size(self,widget, width=450, height=450):
        widget.setMaximumWidth(width)
        widget.setMaximumHeight(height)
        widget.setMinimumHeight(height)
        widget.setMinimumWidth(width)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PatientDashBoard()
    window.show()
    app.exec()