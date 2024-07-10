
from datetime import datetime
import json
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *

from ui.Ui_VentanaPrincipal import Ui_MainWindow
from utils.CheckStatusHBL import checkErrors, getHBLpid, isHBLrunning
from utils.ConfigManager import ConfigManager
from utils.StartOnBoot import disableKioscMode, disableStartOnBoot, enableKioscMode, enableStartOnBoot, isKioscModeEnabled, isStartOnBootEnabled
from utils.Terminal import Terminal
from utils.GetCurrenPath import getRootPath

from ventanas.MyQDialog import MyQDialog
from ventanas.SystemTrayIcon import SystemTrayIcon
from ventanas.MyQtreeWidget import MyQtreeWidget

from pathlib import Path
import os,sys
from enum import Enum

class Estados(Enum):
    CORRIENDO = 0
    DETENIDO  = 1
    REINICIANDO =2
    ERROR = 3

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        image = getRootPath() + "/images/leon.png"
        self.config = ConfigManager(getRootPath() + '/config/userConfig.json')
        self.tray = SystemTrayIcon(QIcon(image),self)
        self.setWindowIcon(QIcon(image))
        
        self.status = Estados.DETENIDO
        
        self.treeFiles = MyQtreeWidget(self.ui.logs_treeWidget)
        self.tray.show()
        
        self.ui.startButton.clicked.connect(self.buttonStart)
        self.ui.stopButton.clicked.connect(self.buttonStop)
        self.ui.updateStatusButton.clicked.connect(self.updateHBLStatus)
        self.ui.saveConfigButton.clicked.connect(self.saveConfig)
        self.ui.openFiles_pushButton.clicked.connect(self.hblPathChanged)
        self.ui.path_lineEdit.setText(self.config.get('hblPath'))
        self.ui.url_lineEdit.setText(self.config.get('kioskURL'))
        self.ui.status_lineEdit.setText(f'Detenido')

        self.readFiles()
        self.updateHBLStatus()
        self.iniciarTimerStatus()
        self.startOnBoot()
        

    def hblPathChanged(self):
        hblPath = self.ui.path_lineEdit.text()
        self.config.update('hblPath',hblPath)
        self.config.save()
        self.startOnBoot()
        self.readFiles()

    def readFiles(self):
        hblPath = self.ui.path_lineEdit.text()
        
        self.treeFiles.tree.clear()
        self.treeFiles.setHBLPath(hblPath)
        try:
            if os.path.exists(f'{hblPath}/logs'):
                logs = os.listdir(os.path.join(hblPath,'logs')) 
                self.treeFiles.addItems('logs',logs)
            if os.path.exists(f'{hblPath}/log'):
                logs = os.listdir(os.path.join(hblPath,'log')) 
                self.treeFiles.addItems('log',logs)
        except Exception as e:
            print(e.__str__())
        
        try:
            if os.path.exists(f'{hblPath}/configuracion/configHBL.json'):
                configFiles = os.listdir(os.path.join(hblPath,'configuracion')) 
                if 'configHBL.json' in configFiles:
                    self.treeFiles.addItems('configuracion',['configHBL.json'])
            elif os.path.exists(f'{hblPath}/modulos/hbl.json'):
                self.treeFiles.addItems('modulos',['hbl.json'])
        except Exception as e:
            print(e.__str__())
        
    
    def buttonStart(self):
        print("start")
        hblPath = self.ui.path_lineEdit.text()
        self.setStatus(Estados.CORRIENDO)
        Terminal(f'cd {hblPath};sudo sh {hblPath}/start.sh')
        
        
    def buttonStop(self):
        print("stop")
        hblPath = self.ui.path_lineEdit.text()
        pid = getHBLpid()
        for id in pid:
            Terminal(f'sudo kill -9 {id}')
        #Terminal(f'sudo sh {hblPath}/stop.sh')

    def buttonReset(self):
        pass
    
    def hblStatus(self):
        pass
    def exit(self):
        self.exit()

    def saveConfig(self):
        startOnboot = self.ui.startOnBoot_checkBox.isChecked()
        kioskMode = self.ui.kioscEnable_checkBox.isChecked()
        hblPath = self.ui.path_lineEdit.text()
        kioskUrl = self.ui.url_lineEdit.text()
        self.config.update('startOnBoot', startOnboot)
        self.config.update('kioskMode',kioskMode)
        self.config.update('kioskURL',kioskUrl)
        self.config.update('hblPath',hblPath)
        self.config.save()

        if startOnboot:
            if not isStartOnBootEnabled(hblPath):
                enableStartOnBoot(hblPath)
        else:
            disableStartOnBoot(hblPath)

        if kioskMode:
            enableKioscMode(kioskUrl)
        else:
            disableKioscMode()

        self.readFiles()
    
    def startOnBoot(self):
        hblPath = self.ui.path_lineEdit.text()
        
        self.ui.startOnBoot_checkBox.setChecked(isStartOnBootEnabled(hblPath))
        self.ui.kioscEnable_checkBox.setChecked(isKioscModeEnabled())

    def updateHBLStatus(self):
        if isHBLrunning():
            self.setStatus(Estados.CORRIENDO)
        
                
        else:
                self.setStatus(Estados.DETENIDO)
    def iniciarTimerStatus(self):
        # Configuración del temporizador
        
        self.timer.timeout.connect(self.updateHBLStatus)
        self.timer.start(5000)  # Intervalo de 5000 ms (5 segundos)

    def detenerTimerStatus(self):
        self.timer.stop()  

    def setStatus(self, statusName):
        if statusName != self.status:
            self.status = statusName
            time = datetime.now().strftime("%H:%M:%S %Y-%m-%d ")
            if statusName == Estados.CORRIENDO:
                self.ui.startButton.setEnabled(False)
                self.ui.stopButton.setEnabled(True)
                self.ui.resetButton.setEnabled(True)
                self.tray.changeStatus('Corriendo')
                self.ui.status_lineEdit.setText(f'Corriendo {time} ')
            elif statusName == Estados.DETENIDO: 
                self.ui.startButton.setEnabled(True)
                self.ui.stopButton.setEnabled(False)
                self.ui.resetButton.setEnabled(False)
                self.tray.changeStatus('Detenido')
                self.ui.status_lineEdit.setText(f'Detenido {time} ')
            elif statusName == Estados.ERROR:
                pass
