import os,sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout

App = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setWindowTitle("C.E.A.R.A.")


                                        ############################################
                                        #      setting things for eGFR Window      #
                                        ############################################

eGFRWindow=QWidget()
eGFRWindow.setWindowTitle("eGFR Calculator")
eGFRWindow.resize(800, 600)
eGFRLayout=QGridLayout(eGFRWindow)










                                                #######################
                                                #   Final Excution    #
                                                #######################
eGFRWindow.show()
MainWindow.show()
App.exec()