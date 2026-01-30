import os,sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QGuiApplication
from eGFRSubWindow import eGFRSubWindow
from ContrastRiskSubWindow import ContrastRiskSubWindow


App = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setWindowTitle("C.E.A.R.A. v0.3")
screen_size=QGuiApplication.primaryScreen().availableGeometry()#availablesize() ignores task bar geometry account for task bar height
screen_width=screen_size.width()
screen_height=screen_size.height()
MainWindow.resize(screen_width,screen_height)

#calling egfr calculator window
eGFRWindow=eGFRSubWindow()
eGFRWindow.adjustSize()
eGFRWindow.move(screen_width-eGFRWindow.width(),0)

#calling mehrane window
CINWindow=ContrastRiskSubWindow()
CINWindow.adjustSize()
CINWindow.move(screen_width-CINWindow.frameGeometry().width(),screen_height-30-CINWindow.frameGeometry().height())




                                                #######################
                                                #   Final Excution    #
                                                #######################
MainWindow.show()
eGFRWindow.show()
CINWindow.show()
eGFRWindow.raise_()
CINWindow.raise_()
App.exec()