import os,sys
from nephrology_equations_module import calculate_eGFR,contrast_risk
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QGridLayout, QLabel, QComboBox, QPushButton
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt

App = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setWindowTitle("C.E.A.R.A. v0.1")
screen_size=QGuiApplication.primaryScreen().availableSize()
screen_width=screen_size.width()
screen_height=screen_size.height()
MainWindow.resize(screen_width,screen_height)

                                        ############################################
                                        #      setting things for eGFR Window      #
                                        ############################################
def egfr_calculate_update_label():
    if egfrAgeLine.text()=="" or egfrAgeLine.text()=="":
        return
    egfr=calculate_eGFR(age=float(egfrAgeLine.text()),cr=float(egfrCrLine.text()),gender=egfrGendercbx.currentText())
    egfrResult2lbl.setText(str(int(egfr))+" cc/min/1.7m\u00B2")
eGFRWindow=QWidget()
eGFRWindow.setWindowTitle("eGFR Calculator")

eGFRWindow.move(screen_width-300,0)
#eGFRWindow.resize(300,150)
eGFRLayout=QGridLayout(eGFRWindow)
eGFRWindow.setLayout(eGFRLayout)
egfrCrlbl=QLabel("Creatinine in mg/dl")
eGFRLayout.addWidget(egfrCrlbl,1,1)

egfrCrLine=QLineEdit()

eGFRLayout.addWidget(egfrCrLine,1,2,1,1)
egfrCrLine.textChanged.connect(egfr_calculate_update_label)

egfrAgelbl=QLabel("Age in Years")
eGFRLayout.addWidget(egfrAgelbl,2,1)
egfrAgeLine=QLineEdit()

eGFRLayout.addWidget(egfrAgeLine,2,2,1,1)
egfrAgeLine.textChanged.connect(egfr_calculate_update_label)

egfrGenderlbl=QLabel("Gender")
eGFRLayout.addWidget(egfrGenderlbl,3,1)
egfrGendercbx=QComboBox()
egfrGendercbx.addItem("Female")
egfrGendercbx.addItem("Male")
eGFRLayout.addWidget(egfrGendercbx,3,2)
egfrGendercbx.currentIndexChanged.connect(egfr_calculate_update_label)

egfrResult1lbl=QLabel("eGFR =")
egfrResult2lbl=QLabel("-- cc/min/1.7m\u00B2")
eGFRLayout.addWidget(egfrResult1lbl,4,1)
eGFRLayout.addWidget(egfrResult2lbl,4,2)

# egfrCalculatebtn=QPushButton("Calculate")
# eGFRLayout.addWidget(egfrCalculatebtn,5,1,1,2)
# egfrCalculatebtn.clicked.connect(egfr_calculate_update_label)





                                                #######################
                                                #   Final Excution    #
                                                #######################
MainWindow.show()
eGFRWindow.show()
eGFRWindow.raise_()

App.exec()