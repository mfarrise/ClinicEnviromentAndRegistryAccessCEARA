
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QListView, QPushButton
import sys

class update_add_visit_selector_widget(QWidget):
    def __init__(self,id,name):
        super().__init__()
        self.id=id
        self.name=name
        layout = QGridLayout()
        self.setLayout(layout)
        label1=QLabel()
        label1.setText("patient selected")
        label2 = QLabel()
        label2.setText(self.name+" "+str(self.id))
        self.new_patient_button = QPushButton("Add visit")
        # self.new_patient_button.clicked.connect(self.add_new_visit)
        self.update_visit_button=QPushButton("Update Visit")
        # self.update_visit_button.clicked.connect(self.update_last_visit)

        layout.addWidget(label1)
        layout.addWidget(label2)

        layout.addWidget(self.new_patient_button)
        layout.addWidget(self.update_visit_button)

