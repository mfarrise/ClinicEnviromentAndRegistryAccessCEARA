import os,sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QPushButton
from PySide6.QtGui import QGuiApplication
from eGFRSubWindow import eGFRSubWindow
from ContrastRiskSubWindow import ContrastRiskSubWindow
from PatientDashBoard import PatientDashBoard


class MainWindow_class(QMainWindow):
    def __init__(self):
        super().__init__()
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
        #finances_button.clicked.connect(self.call_finances)

        layout.addWidget(standard_button)
        layout.addWidget(dash_board_button)
        layout.addWidget(cin_button)
        layout.addWidget(gfr_button)
        layout.addWidget(finances_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.eGFRWindow = eGFRSubWindow()
        self.CINWindow = ContrastRiskSubWindow()
        self.PatientWindow = PatientDashBoard()
        self.screen_size=QGuiApplication.primaryScreen().availableGeometry()#availablesize() ignores task bar geometry account for task bar height
        self.screen_width=self.screen_size.width()
        self.screen_height=self.screen_size.height()


        # self.resize(self.screen_width,self.screen_height)
    def call_standard(self):
        self.call_patient_dashboard()
        self.call_gfr()
        self.call_cin()
    def call_gfr(self):
        #calling egfr calculator window
        self.eGFRWindow.adjustSize()
        self.eGFRWindow.show()
        self.eGFRWindow.raise_()

    def call_cin(self):


        self.CINWindow.show()
        self.CINWindow.raise_()
        self.CINWindow.adjustSize()

    def call_patient_dashboard(self):
        self.PatientWindow.show()
        self.PatientWindow.raise_()



App = QApplication(sys.argv)
MainWindow = MainWindow_class()
MainWindow.setWindowTitle("C.E.A.R.A. v0.3")




                                                #######################
                                                #   Final Excution    #
                                                #######################

MainWindow.show()
App.exec()