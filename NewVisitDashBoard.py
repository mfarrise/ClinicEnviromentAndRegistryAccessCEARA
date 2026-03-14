


import re
import sys
import json
import old_history_viewer

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QLineEdit, QApplication, QTextEdit, \
    QLabel, QComboBox, QMenuBar, QTableWidget, QTableWidgetItem

from SharedWidgetsPyside6 import show_warning
from PySide6.QtGui import  QIntValidator, Qt

from Tool_CreatDataBase import *
from old_history_viewer import OldHistoryViewer


class NewVisitDashBoard(QWidget):
    def __init__(self,id):
        super().__init__()
        self.opened_windows_list=[]
        self.id=id
        # self.setStyleSheet("""
        # QWidget {
        #     background-color: #1e1e1e;
        #     color: white;
        #     font-size: 13px;
        # }
        #
        # QLineEdit, QTextEdit, QComboBox {
        #     background-color: #2b2b2b;
        #     border: 1px solid #3a3a3a;
        #     border-radius: 6px;
        #     padding: 4px;
        # }
        #
        # QPushButton {
        #     background-color: #3a3a3a;
        #     border-radius: 6px;
        #     padding: 6px;
        # }
        #
        # QPushButton:hover {
        #     background-color: #505050;
        # }
        # """)


        #NOTE global declarations
        self.patient_id=0
        self.visit_id=0

        self.settings={}
        quadrant_width=540
        quadrant_height=300
        with open("PatientDashBoard_settings.json","r") as file:
            self.settings=json.load(file)

        with open("clinical_triggers.json","r") as read_json:
            self.clinical_triggers=json.load(read_json)
        # print (self.clinical_triggers)


        iraq_governorates = [
            "Baghdad",
            "Basra",
            "Nineveh",
            "Erbil",
            "Sulaymaniyah",
            "Duhok",
            "Kirkuk",
            "Anbar",
            "Babil",
            "Karbala",
            "Najaf",
            "Wasit",
            "Diyala",
            "Salah al-Din",
            "Maysan",
            "Dhi Qar",
            "Al-Muthanna",
            "Al-Qadisiyyah",
            "other"
        ]
        #NOTE main Layout
        ##############################################################################
        #setting main lay out that will contain 4 Qgridlayouts each for each quadrant#
        ##############################################################################
        self.main_layout = QGridLayout(self)
        # m,s=10,12
        # self.main_layout.setContentsMargins(m,m,m,m)
        # self.main_layout.setSpacing(s)
        self.setLayout(self.main_layout)
        self.move(0, 0)

        self.menu_bar=QMenuBar()
        self.file_menu=self.menu_bar.addMenu("File")
        self.set_directory_action_menu_item=self.file_menu.addAction("Set Directory")
        self.set_directory_action_menu_item.triggered.connect(self.set_directory_for_patient_registry_in_setting_json)
        self.open_old_history_viewer_menu_item=self.file_menu.addAction("view Old History")
        self.open_old_history_viewer_menu_item.triggered.connect(self.open_old_history_viewer)
        self.main_layout.addWidget(self.menu_bar)

        #NOTE ULQ Demographics
        ######################################################################
        #setting up the ULQ which is the patient old history and demographics#
        ######################################################################
        # region

        with sqlite3.connect("ceara.db") as connection:
            cursor=connection.cursor()
            cursor.execute("""SELECT * FROM patients WHERE id=?""",(self.id,))
            self.demo_query_list=cursor.fetchall()
            cursor.execute("""SELECT * from visits where patient_id=?
            ORDER BY visit_date ASC""",(self.id,))
            self.visits_query_list=cursor.fetchall()
            print (self.visits_query_list)
            self.old_history_html=""
            for visit_tuple in self.visits_query_list:
                self.visit_id=visit_tuple[0]#will loop the visit id through all visits and automatically take the last visit id at last
                self.old_history_html +=f"""<div style="text-align:center;"><h3 style='color:red'><b>{visit_tuple[2]}</b><br>"""#Date

                self.old_history_html += """<b>-----------------</b></h3></div>"""

                cursor.execute("""SELECT free_form from visit_free_form_findings where id=?""",
                               (self.visit_id,))
                self.visit_free_form_list=cursor.fetchall()
                self.visit_free_form_str=self.visit_free_form_list[0][0].replace("\n","<br>")
                self.old_history_html +=f"""{self.visit_free_form_str}"""#old_history free form

                self.old_history_html +="""<br>"""
                self.old_history_html +=\
                    """<span style='color:blue'><br><b>Investigations<br>-----------------------</span></b><br>"""

                cursor.execute("""
                SELECT test_name,value,unit,flag FROM visit_investigations WHERE visit_id=?""",
                              (self.visit_id,))
                self.visit_investigations_list=cursor.fetchall()
                for investigation_tuple in self.visit_investigations_list:
                    investigation_list = list(investigation_tuple)
                    investigation_list = [" " if x == "omitted" else x for x in investigation_list]
                    self.old_history_html +=f"""<span style='color:blue'><b>{investigation_list[0]}</b> {investigation_list[1]} {investigation_list[2]}
                     <i>===> </i> {investigation_list[3]}<br></span>"""

                self.old_history_html += \
                    """<span style='color:brown'><br><b>Adjusted Medications<br>---------------------------------</span></b><br>"""

                cursor.execute("""
                                SELECT drug_name,dose,freq,flag,reason FROM visit_adjusted_medications WHERE visit_id=?""",
                               (self.visit_id,))
                self.visit_adjusted_medications_list = cursor.fetchall()
                for adjusted_medications_tuple in self.visit_adjusted_medications_list:
                    adjusted_medications_list = list(adjusted_medications_tuple)
                    adjusted_medications_list = [" " if x == "omitted" else x for x in adjusted_medications_list]
                    self.old_history_html +=f"""<span style='color:brown'><b>{adjusted_medications_list[0]}</b> {adjusted_medications_list[1]} {adjusted_medications_list[2]}
                      I <b>{adjusted_medications_list[3]}</b> it  <i><u>context</u></i> {adjusted_medications_list[4]}<br></span>"""


                self.old_history_html += \
                    """<span style='color:green'><br><b>medications<br>-----------------------</span></b><br>"""

                cursor.execute("""
                                SELECT name,brand,form,dose,freq,note FROM visit_medications WHERE visit_id=?""",
                               (self.visit_id,))
                self.visit_medications_list = cursor.fetchall()

                for medications_tuple in self.visit_medications_list:
                    medications_list=list(medications_tuple)
                    medications_list = [" " if x == "omitted" else x for x in medications_list]

                    self.old_history_html +=f"""<span style='color:green'><b>{medications_list[0]}</b> ({medications_list[1]}) {medications_list[2]}
                      {medications_list[3]} {medications_list[4]} {medications_list[5]}<br></span>"""
                self.old_history_html += """<br>"""




        self.demo_query_list=self.demo_query_list[0]#flatten2d to 1d

        self.patient_demo_and_old_data_widget=QWidget()
        self.patient_demo_and_old_data_layout = QGridLayout(self.patient_demo_and_old_data_widget)
        self.patient_demo_and_old_data_widget.setLayout(self.patient_demo_and_old_data_layout)
        self.set_quadrants_size(self.patient_demo_and_old_data_widget,quadrant_width,quadrant_height)

        self.patient_id_line_edit=QLineEdit()
        self.patient_id_line_edit.setText(str(self.demo_query_list[0]))
        self.patient_id_line_edit.setReadOnly(True)
        self.patient_id_line_edit.setFocusPolicy(Qt.ClickFocus)

        self.patient_name_edit = QLineEdit()
        self.patient_name_edit.setText(self.demo_query_list[1])
        # self.patient_name_edit.editingFinished.connect(self.change_title)
        self.patient_name_edit.setReadOnly(True)
        self.setWindowTitle(self.demo_query_list[1])

        self.patient_DOB_edit = QLineEdit()
        self.patient_DOB_edit.setPlaceholderText("DOB")
        self.now=datetime.now().year
        self.patient_DOB_edit.setValidator(QIntValidator(1900,self.now))
        self.patient_DOB_edit.setText(str(self.demo_query_list[2]))
        self.patient_DOB_edit.setDisabled(True)

        self.patient_age_edit = QLineEdit()
        # self.patient_age_edit.setPlaceholderText("Age")
        self.patient_age_edit.setReadOnly(True)
        self.patient_age_edit.setFocusPolicy(Qt.ClickFocus)
        self.patient_age_edit.setDisabled(True)
        self.calculate_set_age()

        self.patient_gender_combo=QComboBox()
        self.patient_gender_combo.addItems(["Male","Female"])
        self.patient_gender_combo.setCurrentText(self.demo_query_list[3])
        self.patient_gender_combo.setDisabled(True)

        self.patient_marital_combo=QComboBox()
        self.patient_marital_combo.addItems(["Single","Married","Divorced","Widowed"])
        self.patient_marital_combo.setCurrentText(self.demo_query_list[4])
        self.patient_marital_combo.setDisabled(True)

        self.patient_education_combo=QComboBox()
        self.patient_education_combo.addItems(["University","PostGraduate","Institute","Secondary","Primary","None"])
        self.patient_education_combo.setCurrentText(self.demo_query_list[5])
        self.patient_education_combo.setDisabled(True)

        self.patient_job_edit = QLineEdit()
        self.patient_job_edit.setPlaceholderText("Job")
        self.patient_job_edit.setText(self.demo_query_list[6])
        self.patient_job_edit.setDisabled(True)

        self.patient_job_type_combo=QComboBox()
        self.patient_job_type_combo.addItems(["retired","desk/sedentary","light/outdoor","heavy labour","student"])
        self.patient_job_type_combo.setCurrentText(self.demo_query_list[7])
        self.patient_job_type_combo.setDisabled(True)

        self.patient_governorates_combo = QComboBox()
        self.patient_governorates_combo.addItems(iraq_governorates)
        self.patient_governorates_combo.setCurrentText(self.demo_query_list[8])
        self.patient_governorates_combo.setDisabled(True)

        self.patient_residence_free_form_edit=QLineEdit()
        self.patient_residence_free_form_edit.setPlaceholderText("residence")
        if self.demo_query_list[9]:
            self.patient_residence_free_form_edit.setText(self.demo_query_list[9])
        self.patient_residence_free_form_edit.setDisabled(True)

        self.patient_residence_type_combo = QComboBox()
        self.patient_residence_type_combo.addItems(["center","periphery","rural"])
        self.patient_residence_type_combo.setCurrentText(self.demo_query_list[10])
        self.patient_residence_type_combo.setDisabled(True)

        self.patient_tel_line_edit=QLineEdit()
        if self.demo_query_list[11]:
            self.patient_tel_line_edit.setText(self.demo_query_list[11])
        self.patient_tel_line_edit.setReadOnly(True)

        self.patient_demo_and_old_data_layout.addWidget(self.patient_id_line_edit,0,0)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_name_edit,0,1)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_DOB_edit,0,2)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_age_edit,0,3)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_gender_combo,0,4)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_marital_combo,1,0)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_education_combo,1,1)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_job_edit,1,2,1,2)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_job_type_combo,1,4)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_governorates_combo, 2, 0)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_residence_free_form_edit, 2, 1,1,2)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_residence_type_combo,2,3)
        self.patient_demo_and_old_data_layout.addWidget(self.patient_tel_line_edit,2,4)

        #previous history
        # label
        self.previous_history_label = QLabel()
        self.previous_history_label.setText("Previous History")
        self.previous_history_label.setAlignment(Qt.AlignHCenter)
        self.patient_demo_and_old_data_layout.addWidget(self.previous_history_label,3,0)

        #chronic disease lined edit
        self.chronic_disease_line_edit=QLineEdit()
        self.chronic_disease_line_edit.setText(self.demo_query_list[12])
        self.chronic_disease_line_edit.setEnabled(False)
        self.patient_demo_and_old_data_layout.addWidget(self.chronic_disease_line_edit,3,1,1,3)

        #chronic disease lined edit ADD
        self.add_chronic_disease_line_edit=QLineEdit()
        self.add_chronic_disease_line_edit.setPlaceholderText("Add new Dx")
        self.patient_demo_and_old_data_layout.addWidget(self.add_chronic_disease_line_edit,3,4,1,1)
        # previous history
        # text edit
        self.previous_history_edit = QTextEdit()
        self.previous_history_edit.setReadOnly(True)
        self.previous_history_edit.setHtml(self.old_history_html)
        self.patient_demo_and_old_data_layout.addWidget(self.previous_history_edit, 4, 0,1,5)


        self.main_layout.addWidget(self.patient_demo_and_old_data_widget,1,0)


        # endregion
        #NOTE LLQ current clinical
        ##########################################################################
        # setting up the LLQ which is the patient current history and examination#
        ##########################################################################
        #region
        # creat 2nd degree nested two layouts and widget inside the left lower quadrant llQ layout
        self.llql_widget=QWidget()
        self.set_quadrants_size(self.llql_widget, int(quadrant_width / 2), quadrant_height)
        self.llql_layout = QGridLayout()
        self.llql_widget.setLayout(self.llql_layout)

        self.llqr_widget=QWidget()
        self.set_quadrants_size(self.llqr_widget, int(quadrant_width / 2), quadrant_height)
        self.llqr_layout = QGridLayout()
        self.llqr_widget.setLayout(self.llqr_layout)

        self.patient_today_clinical_widget=QWidget()
        self.patient_today_clinical_layout = QGridLayout()
        self.patient_today_clinical_widget.setLayout(self.patient_today_clinical_layout)
        self.set_quadrants_size(self.patient_today_clinical_widget,quadrant_width,quadrant_height)

        self.patient_today_clinical_layout.addWidget(self.llql_widget,0,0)
        self.patient_today_clinical_layout.addWidget(self.llqr_widget, 0, 1)

        #Today history
        #label
        self.today_history_label = QLabel(self)
        self.today_history_label.setText("Today Clinical")
        self.today_history_label.setAlignment(Qt.AlignHCenter)
        self.llql_layout.addWidget(self.today_history_label, 0, 0)

        # Today history
        #text Edit
        self.today_history_edit = QTextEdit(self)
        self.today_history_edit.setReadOnly(False)
        self.today_history_edit.setFocusPolicy(Qt.ClickFocus)
        self.today_history_edit.setTabChangesFocus(True)
        self.llql_layout.addWidget(self.today_history_edit, 1, 0)

        #clinica intellisense GUI not logic
        #line edit
        self.clinical_intellisense_line_edit = QLineEdit()
        self.clinical_intellisense_line_edit.setPlaceholderText("Intellisense")
        self.clinical_intellisense_line_edit.returnPressed.connect(self.clinical_intellisense)
        self.llql_layout.addWidget(self.clinical_intellisense_line_edit, 2, 0)

        #the shell for picked S/S
        self.picked_symptom_label = QLabel(self)
        self.picked_symptom_label.setText("Picked Symptom")
        self.picked_symptom_label.setAlignment(Qt.AlignCenter)

        self.picked_symptom_text_edit = QTextEdit()
        self.picked_symptom_text_edit.setFocusPolicy(Qt.ClickFocus)
        self.picked_symptom_text_edit.setTabChangesFocus(True)

        self.llqr_layout.addWidget(self.picked_symptom_label, 0, 0)
        self.llqr_layout.addWidget(self.picked_symptom_text_edit, 1, 0)

        self.main_layout.addWidget(self.patient_today_clinical_widget,2,0)

        #endregion
        #NOTE RUQ old drugs and investigations
        ###################################################################################
        # setting up the RUQ which is the patient old medication and today investigation  #
        ###################################################################################
        #region

        ##########################################################################################
        #setting up sub sub layout widget called controls to be on the left half of the RUQ#
        ##########################################################################################

        self.patient_old_medication_and_today_investigations_widget = QWidget()
        self.patient_old_medication_and_today_investigations_layout = QGridLayout()
        self.patient_old_medication_and_today_investigations_widget.setLayout(
            self.patient_old_medication_and_today_investigations_layout)
        self.set_quadrants_size(self.patient_old_medication_and_today_investigations_widget, 727, quadrant_height)

        self.old_medication_widget = QWidget()
        self.old_medication_layout = QGridLayout()
        self.old_medication_widget.setLayout(self.old_medication_layout)
        self.set_quadrants_size(self.old_medication_widget, int(786*2/3), quadrant_height)



        #adjusted medications from last visit table
        self.adjusted_medications_label = QLabel()
        self.adjusted_medications_label.setText("Adjusted Medications")
        self.adjusted_medications_label.setAlignment(Qt.AlignCenter)
        self.old_medication_layout.addWidget(self.adjusted_medications_label, 0, 0)

        self.adjusted_medication_table=QTableWidget()
        self.adjusted_medication_table.setRowCount(0)
        self.adjusted_medication_table.setColumnCount(5)
        self.adjusted_medication_table.setAlternatingRowColors(True)
        self.old_medication_layout.addWidget(self.adjusted_medication_table, 1, 0)
        self.adjusted_medication_table.setHorizontalHeaderLabels(["Name","Dose","Freq","Change","Reason"])

        self.creat_new_patient_in_db_button = QPushButton("Add Visit")
        self.creat_new_patient_in_db_button.setFocusPolicy(Qt.ClickFocus)
        self.creat_new_patient_in_db_button.clicked.connect(self.creat_new_patient_in_db)
        self.old_medication_layout.addWidget(self.creat_new_patient_in_db_button, 2, 0)

        self.patient_old_medication_and_today_investigations_layout.addWidget(self.old_medication_widget,0,0)

        ######################################################################
        # setting up sub sub layout widget to be on the right half of the RUQ#
        ######################################################################
        self.today_investigations_widget = QWidget()
        self.today_investigations_layout = QGridLayout()
        self.today_investigations_widget.setLayout(self.today_investigations_layout)
        self.set_quadrants_size(self.today_investigations_widget, int(600*1/3), quadrant_height)

        # today investigations
        # label
        self.today_investigations_label = QLabel()
        self.today_investigations_label.setText("Today Investigations")
        self.today_investigations_label.setAlignment(Qt.AlignHCenter)
        self.today_investigations_layout.addWidget(self.today_investigations_label, 0, 0)

        # today investigations
        # text edit
        self.today_investigations_edit = QTextEdit(self)
        self.today_investigations_edit.setReadOnly(False)
        self.today_investigations_edit.setFocusPolicy(Qt.ClickFocus)
        self.today_investigations_edit.setTabChangesFocus(True)
        self.today_investigations_layout.addWidget(self.today_investigations_edit, 1,0)

        # today investigation intelligent
        # line edit
        self.today_investigations_intellisense_line = QLineEdit(self)
        self.today_investigations_intellisense_line.setPlaceholderText("Intellisense")
        self.today_investigations_intellisense_line.setReadOnly(False)
        self.today_investigations_layout.addWidget(self.today_investigations_intellisense_line, 2,0)
        self.today_investigations_intellisense_line.returnPressed.connect(self.investigation_intellisense)

        self.patient_old_medication_and_today_investigations_layout.addWidget(
            self.today_investigations_widget ,0,1)
        self.main_layout.addWidget(self.patient_old_medication_and_today_investigations_widget, 1, 1)




        #endregion
        #NOTE RLQ medications
        ##########################################################################
        # setting up the RlQ which is the patient current medication             #
        ##########################################################################

        # today medication
        # label

        self.patient_today_medication_widget = QWidget(self)
        self.patient_today_medication_layout = QGridLayout()
        self.patient_today_medication_widget.setLayout(self.patient_today_medication_layout)
        self.set_quadrants_size(self.patient_today_medication_widget, 740, quadrant_height)

        # Last medications == today medications
        # label

        self.today_medications_label = QLabel()
        self.today_medications_label.setText("Today Medications")
        self.today_medications_label.setAlignment(Qt.AlignHCenter)
        self.patient_today_medication_layout.addWidget(self.today_medications_label, 0, 0)

        self.medication_table=QTableWidget()
        self.medication_table.setRowCount(0)
        self.medication_table.setColumnCount(7)
        self.medication_table.setAlternatingRowColors(True)
        self.patient_today_medication_layout.addWidget(self.medication_table, 1, 0)
        self.medication_table.setHorizontalHeaderLabels(["Name","Brand","Form","Dose","Freq","Amount","Note"])

        # today Medication intelligent
        # line edit
        self.today_medication_intellisense_line = QLineEdit(self)
        self.today_medication_intellisense_line.setPlaceholderText("ciprofloxacin (acino) tab 500 mg 1x1 dis 10 after meal ")
        self.today_medication_intellisense_line.setReadOnly(False)
        self.patient_today_medication_layout.addWidget(self.today_medication_intellisense_line, 2, 0, 1, 2)
        self.today_medication_intellisense_line.returnPressed.connect(self.drug_intellisense)
        self.main_layout.addWidget(self.patient_today_medication_widget, 2, 1)

        #NOTE setting tab focus move order
        self.setTabOrder(self.chronic_disease_line_edit, self.clinical_intellisense_line_edit)
        self.setTabOrder( self.clinical_intellisense_line_edit,self.today_investigations_intellisense_line)
        self.setTabOrder(self.today_history_edit, self.clinical_intellisense_line_edit)
        self.setTabOrder(self.picked_symptom_text_edit, self.today_investigations_intellisense_line)
        self.setTabOrder(self.today_investigations_edit, self.today_investigations_intellisense_line)
        self.setTabOrder( self.today_investigations_intellisense_line,self.today_medication_intellisense_line)
        self.setFixedSize(self.sizeHint())

        ######################
        #NOTE creat db tables#
        ######################


        #NOTE engine and functions
        #NOTE
        ##########################################
        #starting writing th engine of the widget#
        ##########################################
        # region
        #NOTE add new patient to data base
    def creat_new_patient_in_db(self):
        #checking if NOT NULL feilds are empty
        if not self.patient_name_edit.text().strip():
            show_warning("patinet name is missing")
            return
        if not self.patient_DOB_edit.text().strip():
            show_warning("patient DOB is missing")
            return
        if not self.today_history_edit.toPlainText().strip():
            show_warning("today history is missing")
            return

        with sqlite3.connect("ceara.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
        INSERT INTO patients
        (patient_name,DOB, gender, marital_state, education, job, job_type,governorate , residence,
        residence_type,telephone,chronic_disease,created_at)
        VALUES (?, ?,?, ?, ?, ?, ?, ?,?,?,?,?,?)
        """, (
            self.patient_name_edit.text(),
            int(self.patient_DOB_edit.text()),
            self.patient_gender_combo.currentText(),
            self.patient_marital_combo.currentText(),
            self.patient_education_combo.currentText(),
            self.patient_job_edit.text(),
            self.patient_job_type_combo.currentText(),
            self.patient_governorates_combo.currentText(),
            self.patient_residence_free_form_edit.text(),
            self.patient_residence_type_combo.currentText(),
            self.patient_tel_line_edit.text(),
            self.chronic_disease_line_edit.text(),
            datetime.now().replace(microsecond=0).isoformat()
            ))
            self.patient_id=cursor.lastrowid
            cursor.execute("""
            INSERT INTO visits
            (patient_id,visit_date,locked,created_at)
            VALUES(?,?,?,?)
        """,(
            self.patient_id,
            datetime.now().date().isoformat(),
            0,
            datetime.now().replace(microsecond=0).isoformat()
            ))
            self.visit_id=cursor.lastrowid
            # print(self.visit_id,self.patient_id)
            if self.today_history_edit.toPlainText().strip():

                cursor.execute("""
                INSERT INTO visit_free_form_findings
                    (visit_id,free_form,created_at)
                    VALUES(?,?,?)
                        """,
                               (
                                   self.visit_id,
                                   self.today_history_edit.toPlainText(),
                                   datetime.now().replace(microsecond=0).isoformat()
                               ))
                print("today history pushed")
            picked_findings_str=self.picked_symptom_text_edit.toPlainText()
            picked_findings_list=picked_findings_str.split("\n")

            if self.picked_symptom_text_edit.toPlainText().strip():

                for raw_finding in picked_findings_list:
                    if raw_finding.strip():#rule out accidental empty lines from manual editing the text edit box
                        keyword,context=raw_finding.split(":")
                        cursor.execute("""
                        INSERT INTO visit_findings
                             (visit_id,keyword,context,created_at)
                            VALUES (?,?,?,?)
                                       """,
                                       (
                                           self.visit_id,
                                           keyword,
                                           context,
                                           datetime.now().replace(microsecond=0).isoformat()
                                       ))
                print("picked symptom pushed")

            if self.today_investigations_edit.toPlainText().strip():
                investigations_str=self.today_investigations_edit.toPlainText()
                investigations_list=investigations_str.split("\n")
                print (investigations_list)
                for raw_investigation in investigations_list:
                    parsed_investigation_list=raw_investigation.split(" ")
                    if len(parsed_investigation_list)<4:# correct non standard input forms
                        for i in range(len(parsed_investigation_list),4):
                            parsed_investigation_list.append("ommited")
                        parsed_investigation_list[3]="unknown"
                        print(parsed_investigation_list)
                    print(parsed_investigation_list,len(parsed_investigation_list))
                    if raw_investigation.strip():#avoid emty lines resulting from manual edit
                        cursor.execute("""
                        INSERT INTO visit_investigations
                            (visit_id,test_name,value,unit,flag,created_at)
                            VALUES(?,?,?,?,?,?)""",
                                       (
                                           self.visit_id,
                                           parsed_investigation_list[0],
                                           parsed_investigation_list[1],
                                           parsed_investigation_list[2],
                                           parsed_investigation_list[3].strip("()"),
                                           datetime.now().replace(microsecond=0).isoformat()
                                       ))
                print("investigation pushed")
            if self.medication_table.item(0,0):
                row_count=self.medication_table.rowCount()
                column_count=self.medication_table.columnCount()

                for row in range(row_count):
                    current_cells_list=[]
                    for column in range(column_count):
                        current_cells_list.append(self.medication_table.item(row, column).text())
                        for i in range(len(current_cells_list)):  # fail safe for empty ,,,replace with " "
                            # print(row_cells_list[i])
                            if not current_cells_list[i].strip():
                                current_cells_list[i] = "omitted"
                            # print(row_cells_list[i])
                    # the logic in the (((IN))) in the following if statements will include words with ed and without
                    #so stop will include stop and stopped
                    if "stop" in current_cells_list[-1] :
                        self.push_to_visit_adjusted_medications(cursor,"stopped",current_cells_list)
                        continue
                    if "increase" in current_cells_list[-1].lower():
                        self.push_to_visit_adjusted_medications(cursor,"increased",current_cells_list)
                        continue
                    if "reduce" in current_cells_list[-1].lower():
                        self.push_to_visit_adjusted_medications(cursor,"reduced",current_cells_list)
                        continue
                    if "decrease" in current_cells_list[-1].lower():
                        self.push_to_visit_adjusted_medications(cursor,"reduced", current_cells_list)
                        continue

                    cursor.execute("""
                    INSERT INTO visit_medications
                        (visit_id,name,brand,form,dose,freq,amount,note,created_at)
                        VALUES(?,?,?,?,?,?,?,?,?)
                            """,
                                   (
                                       self.visit_id,
                                       current_cells_list[0],
                                       current_cells_list[1],
                                       current_cells_list[2],
                                       current_cells_list[3],
                                       current_cells_list[4],
                                       current_cells_list[5],
                                       current_cells_list[6],
                                       datetime.now().replace(microsecond=0).isoformat()
                                   ))
                print("medications pushed")








    def push_to_visit_adjusted_medications(self,cursor,flag,current_cells_list):
        cursor.execute("""
        INSERT INTO visit_adjusted_medications
            (visit_id,drug_name,dose,freq,flag,reason,created_at)
            VALUES(?,?,?,?,?,?,?)
            
        """,
                       (
                           self.visit_id,
                           current_cells_list[0],
                           current_cells_list[3],
                           current_cells_list[4],
                           flag,
                           current_cells_list[6],
                           datetime.now().replace(microsecond=0).isoformat()
                       ))

    def calculate_set_age(self):
        age=self.now-int(self.patient_DOB_edit.text())
        self.patient_age_edit.setText(str(age))

    def open_path_dialog(self):

        file_path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption="Select file",
            dir=self.settings["patient_dir"],#settings is a dictionary read from json this dictionary hold the settings including patient files directory
            filter="All Files (*.*);;Word Files (*.docx);;PDF Files (*.pdf)"
        )
        #print(type(file_path),file_path)
        return file_path

    def set_quadrants_size(self,widget, width=450, height=450):
        widget.setMaximumWidth(width)
        widget.setMaximumHeight(height)
        widget.setMinimumHeight(height)
        widget.setMinimumWidth(width)

    def set_directory_for_patient_registry_in_setting_json(self):
        temp_dir_path=self.pick_directory_name()
        if temp_dir_path:#to check if a path was selected
            self.settings["patient_dir"]=temp_dir_path
            with open("PatientDashBoard_settings.json","w") as file:
                json.dump(self.settings,file,indent=4)

    def pick_directory_name(self):
        dir_path = QFileDialog.getExistingDirectory(
            parent=None,
            caption="Select file",
            dir="",

        )

        print(type(dir_path),dir_path)
        return dir_path

    def investigation_intellisense(self):
        unparsed_text=self.today_investigations_intellisense_line.text()
        self.today_investigations_intellisense_line.clear()# clear feild after value is taken in line above
        parsed_text=unparsed_text.split()

        if len(parsed_text) < 2:
            show_warning("Not a valid test result")
            return  # Not enough data resulting list is 1 word
        if len (parsed_text) ==3:# if things like b urea 15 it ill parse it into b.urea 15 so it wont stay in to 3 element list ["b","urea","15"]
            parsed_text=[parsed_text[0]+"."+parsed_text[1],parsed_text[2]]
            print (parsed_text)
        if not unparsed_text:# dont know why but this line is not functioning
            return
        # try:
        #     float(parsed_text[-1])
        # except ValueError:
        #     show_warning("Please enter a numerical value after test name")
        #     return
        with open("InvestigationDatabase.json","r") as file:
            InvestigationDatabase=json.load(file)

        for case in InvestigationDatabase.values():

            if parsed_text[0] in case["aliases"]:
                self.append_investigation(
                    case["display"],
                    float(parsed_text[-1]),
                    case["high"],
                    case["low"],
                    case["unit"]
                )
                return
        self.today_investigations_edit.append(unparsed_text)
    def append_investigation(self,test_name,test_value,upper_limit,lower_limit,unit):
        if test_value > upper_limit:
            self.today_investigations_edit.append(
                f"<span style='color:rgb(200,110,110)' ><b>{test_name+' ' + str(test_value) + ' ' +unit+' (high)'}</b></span>"
            )
        elif test_value < lower_limit:
            self.today_investigations_edit.append(
                f"<span style='color:rgb(200,110,110)' ><b>{test_name + ' ' + str(test_value) + ' ' + unit + ' (low)'}</b></span>"
            )
        else :
            self.today_investigations_edit.append(
                f"<span ><b>{test_name + ' ' + str(test_value) + ' ' + unit + ' (normal)'}</b></span>"
            )

    def drug_intellisense(self):

        drug_name_DIC = {
            "name": "",
            "Brand": "",
            "Form": "",
            "Dose": "",
            "Freq": "",
            "Amount": "",
            "Note": ""
        }

        unparsed_phrase = self.today_medication_intellisense_line.text()
        self.today_medication_intellisense_line.clear()

        if unparsed_phrase:
            parsed_drug = unparsed_phrase.split()
            drug_name_DIC["name"] = parsed_drug[0]
            # print(unparsed_phrase)
            dose_picked = False

            for i, word in enumerate(parsed_drug):
                if word[0] == "(" and word[-1] == ")":
                    drug_name_DIC["Brand"] = word.strip("()")

                if word.lower() in ["tab", "vial", "ampule", "cap", "capsule", "tsf", "effervescent", "satchet"]:
                    drug_name_DIC["Form"] = word

                dose_pattern = r'^-?\d+(\.\d+)?$'
                if re.match(dose_pattern, word) and not dose_picked:
                    drug_name_DIC["Dose"] = word + " " + parsed_drug[i + 1]
                    dose_picked = True  # avoid picking any digit words in the notes or number for dis

                if "x" in word.lower() and word[0].isdigit() and word[-1].isdigit() and len(word) == 3:
                    drug_name_DIC["Freq"] = word
                if word.lower() == "dis":
                    drug_name_DIC["Amount"] = parsed_drug[i + 1]
                    note = ""
                    for t in range(i + 2, len(parsed_drug)):
                        note += parsed_drug[t]
                        note += " "
                    drug_name_DIC["Note"] = note
                    pass


            print("new row created")
            row_number=self.medication_table.rowCount()
            self.medication_table.insertRow(row_number)

            #ill implement transfering the dictionary to the new row using row_number in row place
            for i,key in enumerate(drug_name_DIC.keys()):
                item = QTableWidgetItem(drug_name_DIC[key])
                item.setTextAlignment(Qt.AlignCenter)
                self.medication_table.setItem(row_number, i, item)

    def old_drug_intellisense(self):

        drug_name_DIC = {
            "name": "",
            "Form": "",
            "Dose": "",
            "Freq": ""
        }

        unparsed_phrase = self.old_medication_intellisense_line.text()
        self.old_medication_intellisense_line.clear()

        if unparsed_phrase:
            parsed_drug = unparsed_phrase.split()
            drug_name_DIC["name"] = parsed_drug[0]
            # print(unparsed_phrase)
            dose_picked = False

            for i, word in enumerate(parsed_drug):

                if word.lower() in ["tab", "vial", "ampule", "cap", "capsule", "tsf", "effervescent", "satchet"]:
                    drug_name_DIC["Form"] = word

                dose_pattern = r'^-?\d+(\.\d+)?$'
                if re.match(dose_pattern, word) and not dose_picked:
                    drug_name_DIC["Dose"] = word + " " + parsed_drug[i + 1]
                    dose_picked = True  # avoid picking any digit words in the notes or number for dis

                if "x" in word.lower() and word[0].isdigit() and word[-1].isdigit() and len(word) == 3:
                    drug_name_DIC["Freq"] = word




            print("new row created")
            row_number=self.old_medication_table.rowCount()
            self.old_medication_table.insertRow(row_number)

            #ill implement transfering the dictionary to the new row using row_number in row place
            for i,key in enumerate(drug_name_DIC.keys()):
                item = QTableWidgetItem(drug_name_DIC[key])
                item.setTextAlignment(Qt.AlignCenter)
                self.old_medication_table.setItem(row_number, i, item)

    def clinical_intellisense(self):

        temp_clinical_phrase=self.clinical_intellisense_line_edit.text().lower()
        print(temp_clinical_phrase)
        self.today_history_edit.append(temp_clinical_phrase)
        for key in self.clinical_triggers.keys():
            for value in self.clinical_triggers[key]:
                lower_value = value.lower()
                if lower_value in temp_clinical_phrase:
                    # temp_clinical_phrase = temp_clinical_phrase.replace(lower_value, "")
                    # temp_clinical_phrase = " ".join(temp_clinical_phrase.split())
                    if key=="blood_pressure":
                        blood_pressure=temp_clinical_phrase.replace(lower_value,"")
                        blood_pressures = blood_pressure.split("/")
                        self.picked_symptom_text_edit.append("<span style=color:#ED7672><b>systolic bp: </b></span>"+blood_pressures[0])
                        self.picked_symptom_text_edit.append("<span style=color:#ED7672><b>diastolic bp: </b></span>" + blood_pressures[1])
                        break
                    self.picked_symptom_text_edit.append(f"<span style=color:#ED7672><b>{key}: </b></span>"+temp_clinical_phrase)

                    break
        self.clinical_intellisense_line_edit.clear()

    def change_title(self):
        if self.patient_name_edit.text():
            self.setWindowTitle(self.patient_name_edit.text()+" new patient")

    def open_old_history_viewer(self):
        old_history_viewer_window=OldHistoryViewer(self.patient_name_edit.text(),self.old_history_html)
        old_history_viewer_window.show()
        self.opened_windows_list.append(old_history_viewer_window)

#TODO ((done but))mental note to expand and revist the dictionary in json creation tool for the symptoms



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NewVisitDashBoard(4)
    window.show()
    app.exec()
