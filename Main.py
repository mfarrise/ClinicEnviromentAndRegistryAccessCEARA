import os,sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QGuiApplication
from eGFRSubWindow import eGFRSubWindow
from ContrastRiskSubWindow import ContrastRiskSubWindow


App = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setWindowTitle("C.E.A.R.A. v0.3")
screen_size=QGuiApplication.primaryScreen().availableSize()
screen_width=screen_size.width()
screen_height=screen_size.height()
MainWindow.resize(screen_width,screen_height)

#calling egfr calculator window
eGFRWindow=eGFRSubWindow()
eGFRWindow.move(screen_width-300,0)

#calling mehrane window
CINWindow=ContrastRiskSubWindow()
CINWindow.move(screen_width-300,screen_height-400)




                                                #######################
                                                #   Final Excution    #
                                                #######################
MainWindow.show()
eGFRWindow.show()
CINWindow.show()
eGFRWindow.raise_()
CINWindow.raise_()
App.exec()