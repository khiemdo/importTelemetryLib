# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\PersistentStorageApp.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PersistentStorageWidget(object):
    def setupUi(self, PersistentStorageWidget):
        PersistentStorageWidget.setObjectName(_fromUtf8("PersistentStorageWidget"))
        PersistentStorageWidget.resize(859, 683)
        self.verticalLayoutWidget = QtGui.QWidget(PersistentStorageWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 872, 661))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.MainVerticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.MainVerticalLayout.setObjectName(_fromUtf8("MainVerticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.MainVerticalLayout.addWidget(self.label)
        self.PersistentStorageTreeView = QtGui.QTreeView(self.verticalLayoutWidget)
        self.PersistentStorageTreeView.setObjectName(_fromUtf8("PersistentStorageTreeView"))
        self.MainVerticalLayout.addWidget(self.PersistentStorageTreeView)
        self.HorizontalBtnsLayout = QtGui.QHBoxLayout()
        self.HorizontalBtnsLayout.setContentsMargins(251, -1, 43, 29)
        self.HorizontalBtnsLayout.setObjectName(_fromUtf8("HorizontalBtnsLayout"))
        self.LoadPersistentStorageFromRemoteBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.LoadPersistentStorageFromRemoteBtn.setObjectName(_fromUtf8("LoadPersistentStorageFromRemoteBtn"))
        self.HorizontalBtnsLayout.addWidget(self.LoadPersistentStorageFromRemoteBtn)
        self.LoadPersistentStorageFromLocalBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.LoadPersistentStorageFromLocalBtn.setObjectName(_fromUtf8("LoadPersistentStorageFromLocalBtn"))
        self.HorizontalBtnsLayout.addWidget(self.LoadPersistentStorageFromLocalBtn)
        self.SavePersistentStorageToRemoteBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.SavePersistentStorageToRemoteBtn.setObjectName(_fromUtf8("SavePersistentStorageToRemoteBtn"))
        self.HorizontalBtnsLayout.addWidget(self.SavePersistentStorageToRemoteBtn)
        self.SavePersistentStorageToLocalBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.SavePersistentStorageToLocalBtn.setObjectName(_fromUtf8("SavePersistentStorageToLocalBtn"))
        self.HorizontalBtnsLayout.addWidget(self.SavePersistentStorageToLocalBtn)
        self.MainVerticalLayout.addLayout(self.HorizontalBtnsLayout)

        self.retranslateUi(PersistentStorageWidget)
        QtCore.QMetaObject.connectSlotsByName(PersistentStorageWidget)

    def retranslateUi(self, PersistentStorageWidget):
        PersistentStorageWidget.setWindowTitle(_translate("PersistentStorageWidget", "Form", None))
        self.label.setText(_translate("PersistentStorageWidget", "Persistent Storage Treeview", None))
        self.LoadPersistentStorageFromRemoteBtn.setText(_translate("PersistentStorageWidget", "Load from Controller", None))
        self.LoadPersistentStorageFromLocalBtn.setText(_translate("PersistentStorageWidget", "Load from Disk", None))
        self.SavePersistentStorageToRemoteBtn.setText(_translate("PersistentStorageWidget", "Save to Controller", None))
        self.SavePersistentStorageToLocalBtn.setText(_translate("PersistentStorageWidget", "Save to Disk", None))

