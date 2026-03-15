





    #TODO better windows location when are called ((non fixed and breakable))

    #TODO better main window move integrate with standered option button wndows((also non breakable))



import os,sys
import sqlite3

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QPushButton
from PySide6.QtGui import QGuiApplication
from eGFRSubWindow import eGFRSubWindow
from ContrastRiskSubWindow import ContrastRiskSubWindow
from NewPatientDashBoard import NewPatientDashBoard
from Finances import Finances




class MainWindow_class(QMainWindow):
    def __init__(self):
        super().__init__()

        self.daughter_windows_new_patient=[]
        self.connect = sqlite3.connect("ceara.db")
        self.screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setFixedSize(280,295)
        self.setCentralWidget(central_widget)

        standard_button=QPushButton("Standard")
        standard_button.clicked.connect(self.call_standard)
        self.add_new_patient_button = QPushButton("New Patient")
        self.add_new_patient_button.clicked.connect(self.call_new_patient_dashboard)
        cin_button=QPushButton("CIN")
        cin_button.clicked.connect(self.call_cin)
        gfr_button=QPushButton("GFR")
        gfr_button.clicked.connect(self.call_gfr)
        finances_button=QPushButton("Finances")
        finances_button.clicked.connect(self.call_finances)

        layout.addWidget(standard_button)
        layout.addWidget(self.add_new_patient_button)
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


        # self.resize(self.screen_width,self.screen_height)
    def call_standard(self):
        screen = QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()

        width = available_geometry.width()
        height = available_geometry.height()
        frame_rect = self.frameGeometry()
        frame_rect.moveCenter(self.screen_geometry.bottomRight())
        self.move(width,height-695)

        self.call_new_patient_dashboard()
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


    def call_new_patient_dashboard(self):

        new_patient_Window = NewPatientDashBoard()
        self.daughter_windows_new_patient.append(new_patient_Window)
        new_patient_Window.show()
        new_patient_Window.raise_()

    def call_finances(self):
        self.financesWindow.show()
        frame_rect = self.financesWindow.frameGeometry()
        frame_rect.moveCenter(self.screen_geometry.center())
        self.financesWindow.move(frame_rect.topLeft())
        self.financesWindow.raise_()

App = QApplication(sys.argv)
App.setStyleSheet("""
        QWidget {
            background-color: #e3e5e7;
            color: #505255;
            font-size: 13px;
            font-weight: bold;
            font-family: "Ubuntu";
        }

        QLineEdit, QTextEdit, QComboBox {
            background-color: #e3e5e7;
            border: 1px solid #a2a4a5;
            border-radius: 9px;
            padding: 4px;
        }

        QComboBox::drop-down {
        border: none;
        width: 18px;
        }

        QPushButton {
            background-color: #f0f0f0 ;
            border: 1px solid #a2a4a5;
            padding: 6px;
            border-radius: 9px;
        }

        QPushButton:hover {
            background-color: #f5f5f6;
        }

        """)
MainWindow = MainWindow_class()
MainWindow.setWindowTitle("C.E.A.R.A. v0.6")




                                                #######################
                                                #   Final Excution    #
                                                #######################


App.exec()


"""
Funtion
########
the main window from which u can call all the functional windows
and when u call the standard layout which contain 3 windows the main window move it self from 
the center to the right to integrate with other windows

Possible improvements
######################
implement better routines for positioning of the windows and the movement of the main window to the right
"""