import logging
from PyQt4 import QtCore, QtGui, QtXml
from PersistentStorageViewer import PersistentStorageViewer
from PersistentStorageModel import PersistentStorageModel
from SerialController import SerialController
import sys


class PersistentStorageApp():
    def __init__(self):
        self.logger = logging.getLogger("PersistentStorageApp")
        self.app = QtGui.QApplication(sys.argv)
        self.viewer = PersistentStorageViewer()
        self.model = None
        self.serialController = SerialController()
        self.xmlDefaultPath = './python/configurationDef.xml'
        
    def LoadConfigsFromDisk(self, xmlPath):
        import lxml.etree as ET
        psDom = None
        try:
            psDom = ET.parse(xmlPath)
        except Exception as e:
            self.logger.exception("Config file path is invalid")
        finally:
            return psDom
    def LoadConfigsFromControllerHandler(self):
        pass
    def LoadConfigsFromDiskHandler(self):
        #open directoryBox or loadDefault
        filePath = QtGui.QFileDialog.getOpenFileName(self.viewer, "Open File","./python", "XML files (*.xml);;")
        if(filePath):
            self.model = PersistentStorageModel(self.LoadConfigsFromDisk(filePath))                
        else:
            self.model = PersistentStorageModel(self.LoadConfigsFromDisk(self.xmlDefaultPath))#default ConfigPath
        self.viewer.PersistentStorageTreeView.setModel(self.model)
        self.viewer.show()
    def SaveConfigsToControllerHandler(self):
        self.serialController.SetModel(self.model)
        self.serialController.ComposeFormatStringForCStructure()
    def SaveConfigsToDiskHandler(self):
        #open directoryBox or loadDefault
        fileName = QtGui.QFileDialog.getSaveFileName(self.viewer, "Save File","./python","XML files (*.xml);;");
        self.model.domDocument.write(fileName)
    def setup(self):
        #self.viewer.PersistentStorageTreeView.setModel(self.model)
        self.viewer.LoadPersistentStorageFromLocalBtn.clicked.connect(self.LoadConfigsFromDiskHandler)
        self.viewer.LoadPersistentStorageFromRemoteBtn.clicked.connect(self.LoadConfigsFromControllerHandler)
        self.viewer.SavePersistentStorageToRemoteBtn.clicked.connect(self.SaveConfigsToControllerHandler)
        self.viewer.SavePersistentStorageToLocalBtn.clicked.connect(self.SaveConfigsToDiskHandler)
        self.viewer.show()
    def run(self):       
        self.app.exec_()
        self.logger.info("true")



if __name__ == '__main__':
    myApp = PersistentStorageApp()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("hello")
    myApp.setup()
    myApp.run()