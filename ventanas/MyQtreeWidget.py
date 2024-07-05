from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *

from utils.Terminal import Terminal
from ventanas.MyQDialog import MyQDialog

import os


class MyQtreeWidget(QTreeWidget):

    def __init__(self, tree : QTreeWidget, logPath = None) -> None:
        QTreeWidget.__init__(self) 
        self.tree = tree
        self.logPath = logPath
        self.tree.setColumnCount(2)
        self.tree.header().setSectionResizeMode(0,QHeaderView.Stretch)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.showRightClickMenu)
        self.tree.setHeaderLabels(["Files",'ext'])
        
    def addItems(self,name : str, list : [str]): # type: ignore
        key = QTreeWidgetItem([name])
        items = [key]
        
        for l in list:
            try:
                name, ext = l.split('.')
                key.addChild(QTreeWidgetItem([name,ext]))
            except:
                pass
        
        self.tree.insertTopLevelItems(0,items)
        
        self.tree.expandItem(key) 
    


    def showRightClickMenu(self, position):
            clicked_item = self.tree.itemAt(position)
            print(clicked_item.text(0))
            if clicked_item:
                # Crear el menú
                menu = QMenu(self)
                
                # Agregar acciones al menú
                action1 = QAction("Open", self)
                action2 = QAction("Open with vscode", self)
                menu.addAction(action1)
                menu.addAction(action2)
                
                # Conectar las acciones a funciones
                action1.triggered.connect(lambda: self.open_triggered(clicked_item))
                action2.triggered.connect(lambda: self.openWithCode_triggered(clicked_item))
                
                # Mostrar el menú en la posición del cursor
                menu.exec_(self.tree.viewport().mapToGlobal(position))
    
    def setHBLPath(self, path):
        self.path = path

    def open_triggered(self,item : QTreeWidgetItem):
        #subprocess.run(['lxterminal','--command','tail -f /home/pi/Desktop/Hbl3.0/logs/wvdial.log','--hold'])
        
        if item.text(1)=='log':
            #os.system(f'/usr/bin/lxterminal -t {item.text(0)}.log -e tail -f {self.logPath}/logs/{item.text(0)}.log ')
            Terminal(f'/usr/bin/lxterminal -t {item.text(0)}.log -e tail -f {self.path}/{item.parent().text(0)}/{item.text(0)}.log ')
        else:
            Terminal(f'/usr/bin/lxterminal -t {item.text(0)}.{item.text(1)} -e sudo nano {self.path}/{item.parent().text(0)}/{item.text(0)}.{item.text(1)} ')
        #print(f'{self.logPath}/{item.text(0)}.{item.text(1)}')
        
        
            
    def openWithCode_triggered(self,item : QTreeWidgetItem):
        Terminal(f'/usr/bin/lxterminal -e code {self.path}/{item.parent().text(0)}/{item.text(0)}.{item.text(1)} ')
 
    