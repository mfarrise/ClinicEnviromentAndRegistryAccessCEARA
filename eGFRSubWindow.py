import sys

from PySide6.QtCore import QLocale
from PySide6.QtGui import QDoubleValidator, QIntValidator

from nephrology_equations_module import calculate_eGFR
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QComboBox, QWidget, QPushButton, QApplication


class eGFRSubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.clipboard = QApplication.clipboard()


        self.setWindowTitle("eGFR Calculator")

        #self.resize(300,150)
        self.eGFRLayout=QGridLayout()
        self.setLayout(self.eGFRLayout)
        self.egfrCrlbl=QLabel("Creatinine in mg/dl")
        self.eGFRLayout.addWidget(self.egfrCrlbl,1,1)

        self.egfrCrLine=QLineEdit()
        double_validator = QDoubleValidator(0.00,40.00,2)
        double_validator.setLocale(QLocale(QLocale.English))
        self.egfrCrLine.setValidator(double_validator)
        self.eGFRLayout.addWidget(self.egfrCrLine,1,2,1,1)
        self.egfrCrLine.textChanged.connect(self.egfr_calculate_update_label)

        self.egfrAgelbl=QLabel("Age in Years")
        self.eGFRLayout.addWidget(self.egfrAgelbl,2,1)
        self.egfrAgeLine=QLineEdit()
        self.egfrAgeLine.setValidator(QIntValidator(15,120))
        self.eGFRLayout.addWidget(self.egfrAgeLine,2,2,1,1)
        self.egfrAgeLine.textChanged.connect(self.egfr_calculate_update_label)

        self.egfrGenderlbl=QLabel("Gender")
        self.eGFRLayout.addWidget(self.egfrGenderlbl,3,1)
        self.egfrGendercbx=QComboBox()
        self.egfrGendercbx.addItem("Female")
        self.egfrGendercbx.addItem("Male")
        self.eGFRLayout.addWidget(self.egfrGendercbx,3,2)
        self.egfrGendercbx.currentIndexChanged.connect(self.egfr_calculate_update_label)

        self.egfrResult1lbl=QLabel("eGFR =")
        self.egfrResult2lbl=QLabel("-- cc/min/1.7m\u00B2")
        self.eGFRLayout.addWidget(self.egfrResult1lbl,4,1)
        self.eGFRLayout.addWidget(self.egfrResult2lbl,4,2)

        self.egfrCalculatebtn=QPushButton("Copy and Clear")
        self.eGFRLayout.addWidget(self.egfrCalculatebtn,5,1,1,2)
        self.egfrCalculatebtn.clicked.connect(self.clear)

    def egfr_calculate_update_label(self):
        if not self.egfrAgeLine.text()  or not self.egfrCrLine.text():
            return
        egfr = calculate_eGFR(age=float(self.egfrAgeLine.text()), cr=float(self.egfrCrLine.text()),
                              gender=self.egfrGendercbx.currentText())
        self.egfrResult2lbl.setText(str(int(egfr)) + " cc/min/1.7m\u00B2")
        self.clipboard.setText(str(int(egfr)))


    def clear(self):

        if not self.egfrAgeLine.text()  or not self.egfrCrLine.text():
            return
        egfr = calculate_eGFR(age=float(self.egfrAgeLine.text()), cr=float(self.egfrCrLine.text()),
                              gender=self.egfrGendercbx.currentText())
        self.clipboard.setText(str(int(egfr))) #redundant because its already in clipboard but for safety
        self.egfrResult2lbl.setText("--"+" cc/min/1.7m\u00B2")
        self.egfrAgeLine.setText("")
        self.egfrCrLine.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = eGFRSubWindow()
    window.show()
    app.exec()