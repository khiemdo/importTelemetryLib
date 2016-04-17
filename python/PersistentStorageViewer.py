import Ui_PersistentStorageWidget
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging
import sys

class PersistentStorageViewer(QWidget,Ui_PersistentStorageWidget.Ui_PersistentStorageWidget): 
    def __init__(self,parent=None):
        self.logger = logging.getLogger("PersistentStorageViewer")
        super(PersistentStorageViewer,self).__init__(parent)
        self.setupUi(self)
    def test(self):
        self.PersistentStorageTreeView.setModel()
        pass
   
    