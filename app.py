from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *


from ventanas.VentanaPrincipal import VentanaPrincipal

import os

os.environ["DISPLAY"]=':0'
#print(os.environ["DISPLAY"])

app = QApplication([])
app.processEvents()
app.setQuitOnLastWindowClosed(False)
w = VentanaPrincipal()

w.show()
app.exec()


