from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *





class SystemTrayIcon( QSystemTrayIcon):
    def __init__(self, icon, parent = None):
        QSystemTrayIcon.__init__(self,icon,parent)
        menu = QMenu(parent)
        self.setVisible(True)
        prefs_action = menu.addAction('Abrir')
        
        self.status = menu.addAction('...')
        #self.status.setFont(QFont("Arial", 12, QFont.Bold))
        menu.addSeparator()
        self.setContextMenu(menu)
        prefs_action.triggered.connect(self.setPrefs)

    def setPrefs(self):
        
        self.parent().show()

    def changeStatus(self,status):
        
        self.status.setText(status)
