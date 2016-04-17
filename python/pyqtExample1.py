#!/usr/bin/python
# -*- coding: utf-8 -*-
#sys.path.append("./python")
from SerialController import SerialController
from SimpleViewer import SimpleViewer
from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import json
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from builtins import print

def window1():
    app = QApplication(sys.argv)
    win = QWidget()
    e1 = QLineEdit()
    e1.setValidator(QIntValidator())
    e1.setMaxLength(4)
    e1.setAlignment(Qt.AlignRight)
    e1.setFont(QFont("Arial",20))
    e2 = QLineEdit()
    e2.setValidator(QDoubleValidator(0.99,99.99,2))
    flo = QFormLayout()
    flo.addRow("integer validator", e1)
    flo.addRow("Double validator",e2)
    e3 = QLineEdit()
    e3.setInputMask('+99_9999_999999')
    flo.addRow("Input Mask",e3)
    e4 = QLineEdit()
    e4.textChanged.connect(textchanged)
    flo.addRow("Text changed",e4)
    e5 = QLineEdit()
    e5.setEchoMode(QLineEdit.Password)
    flo.addRow("Password",e5)
    e6 = QLineEdit("Hello Python")
    e6.setReadOnly(True)
    flo.addRow("Read Only",e6)
    e5.editingFinished.connect(enterPress)
    win.setLayout(flo)
    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())

def textchanged(text):
    print("contents of text box: " + text)

def enterPress():
   print("edited")

def OnTreeViewItemChangedHandler(item, column):
    print("edited")

def fill_item(item, value):
    item.setExpanded(True)
    if type(value) is dict:
        for key, val in sorted(value.items()):
            child = QTreeWidgetItem()
            child.setFlags(child.flags() | (Qt.ItemIsEditable) | (Qt.ItemIsEnabled))
            child.setText(0, str(key))
            item.addChild(child)
            fill_item(child, val)
    elif type(value) is list:
        for val in value:
            child = QTreeWidgetItem()
            child.setFlags(child.flags() | (Qt.ItemIsEditable) | (Qt.ItemIsEnabled))
            item.addChild(child)
            if type(val) is dict:      
                child.setText(0, '[dict]')
                fill_item(child, val)
            elif type(val) is list:
                child.setText(0, '[list]')
                fill_item(child, val)
            else:
                child.setText(0, str(val))              
                child.setExpanded(True)
    else:
        child = QTreeWidgetItem()
        child.setFlags(child.flags() | (Qt.ItemIsEditable) | (Qt.ItemIsEnabled))
        child.setText(0, str(value))
        item.addChild(child)

def fill_widget(widget, value):
  widget.clear()
  fill_item(widget.invisibleRootItem(), value)

d = { 'key1': 'value1', 
  'key2': 'value2',
  'key3': [1,2,3, { 1: 3, 7 : 9}],
  'key4': object(),
  'key5': { 'another key1' : 'another value1',
            'another key2' : 'another value2'} }

def main():
    controller = SerialController()
    viewer = SimpleViewer()
    controller.LoadDefaultConfigsFromXML()
    app = QApplication(sys.argv)
    win = QWidget()
    verticalLayout = QVBoxLayout()
    verticalLayout.setObjectName("veticalLayout")
    treeView = QTreeWidget()
    treeView.setObjectName("treeView")
    treeView.itemChanged.connect(OnTreeViewItemChangedHandler)
    fill_widget(treeView, controller.persistantStorage)
    verticalLayout.addWidget(treeView)
    okBtn = QPushButton()
    okBtn.setGeometry(QRect(QPoint(100, 100),QSize(200, 50)));
    okBtn.setText("OK")
    okBtn.clicked.connect(OnTreeViewItemChangedHandler)
    verticalLayout.addWidget(okBtn)
    win.setLayout(verticalLayout)
    win.setWindowTitle("EmbeddedPersisttantStorageApp")
    win.show()
    sys.exit(app.exec_())
'''
        controller = SerialController()
        viewer = SimpleViewer()
        transport = SerialTransport()
        tlm = Pytelemetry(transport)
        transport.connect({'port': "com20", 'baudrate': 9600})
'''     


if __name__ == '__main__':
    main()



