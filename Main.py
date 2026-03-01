import os,sys
import sqlite3

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QPushButton
from PySide6.QtGui import QGuiApplication
from eGFRSubWindow import eGFRSubWindow
from ContrastRiskSubWindow import ContrastRiskSubWindow
from PatientDashBoard import PatientDashBoard
from Finances import Finances

class MainWindow_class(QMainWindow):
    def __init__(self):
        super().__init__()

        self.connect = sqlite3.connect("ceara.db")
        self.screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        self.setWindowTitle("C.E.A.R.A. v0.3")
        central_widget = QWidget()
        layout = QVBoxLayout()

        standard_button=QPushButton("Standard")
        standard_button.clicked.connect(self.call_standard)
        dash_board_button = QPushButton("Dash Board")
        dash_board_button.clicked.connect(self.call_patient_dashboard)
        cin_button=QPushButton("CIN")
        cin_button.clicked.connect(self.call_cin)
        gfr_button=QPushButton("GFR")
        gfr_button.clicked.connect(self.call_gfr)
        finances_button=QPushButton("Finances")
        finances_button.clicked.connect(self.call_finances)

        layout.addWidget(standard_button)
        layout.addWidget(dash_board_button)
        layout.addWidget(cin_button)
        layout.addWidget(gfr_button)
        layout.addWidget(finances_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.eGFRWindow = eGFRSubWindow()
        self.CINWindow = ContrastRiskSubWindow()

        self.financesWindow = Finances()

        self.screen_size=QGuiApplication.primaryScreen().availableGeometry()#availablesize() ignores task bar geometry account for task bar height
        self.screen_width=self.screen_size.width()
        self.screen_height=self.screen_size.height()

        self.show()

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(self.screen_geometry.center())
        self.move(window_geometry.topLeft())

        #just testing passing dn connect and passing window title in multiple windows
        self.patient_dashboard_windows=[]
        self.title_int=1
        # self.resize(self.screen_width,self.screen_height)
    def call_standard(self):
        self.call_patient_dashboard()
        self.call_gfr()
        self.call_cin()
    def call_gfr(self):
        #calling egfr calculator window

        self.eGFRWindow.show()
        frame_rect = self.eGFRWindow.frameGeometry()
        frame_rect.moveCenter(self.screen_geometry.topRight())
        self.eGFRWindow.move(frame_rect.topLeft())
        self.eGFRWindow.raise_()

    def call_cin(self):

        self.CINWindow.show()
        frame_rect=self.CINWindow.frameGeometry()
        frame_rect.moveCenter(self.screen_geometry.bottomRight())
        self.CINWindow.move(frame_rect.topLeft())

        self.CINWindow.raise_()


    def call_patient_dashboard(self):
        self.title_int +=1
        # new_patientWindow = PatientDashBoard(self.connect,"patient no "+str(self.title_int))
        new_patientWindow = PatientDashBoard()
        self.patient_dashboard_windows.append(new_patientWindow)
        new_patientWindow.show()
        new_patientWindow.raise_()

    def call_finances(self):
        self.financesWindow.show()
        frame_rect = self.financesWindow.frameGeometry()
        frame_rect.moveCenter(self.screen_geometry.center())
        self.financesWindow.move(frame_rect.topLeft())
        self.financesWindow.raise_()

App = QApplication(sys.argv)
MainWindow = MainWindow_class()
MainWindow.setWindowTitle("C.E.A.R.A. v0.5")




                                                #######################
                                                #   Final Excution    #
                                                #######################


App.exec()