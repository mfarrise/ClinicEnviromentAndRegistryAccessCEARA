import os,sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QGuiApplication
from eGFRSubWindow import eGFRSubWindow

App = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setWindowTitle("C.E.A.R.A. v0.1")
screen_size=QGuiApplication.primaryScreen().availableSize()
screen_width=screen_size.width()
screen_height=screen_size.height()
MainWindow.resize(screen_width,screen_height)

#calling egfr calculator window
eGFRWindow=eGFRSubWindow()
eGFRWindow.move(screen_width-300,0)






                                                #######################
                                                #   Final Excution    #
                                                #######################
MainWindow.show()
eGFRWindow.show()
eGFRWindow.raise_()

App.exec()