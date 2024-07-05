from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *


class MyQDialog(QMessageBox):

    def __init__(self):
        QMessageBox.__init__(self)

    def showAlert(self,title,message):
        self.critical(
            self,
            title,
            message,
            buttons=QMessageBox.Ok
        )
        