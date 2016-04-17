from PyQt4 import QtCore, QtGui, QtXml
import xmltodict
import json
import sip

import logging

class DomItem(object):
    def __init__(self, node, row=0, parent=None):
        # node=ET._Element()
        self.domNode = node
        self.parentItem = parent
        self.rowNumber = row
        self.childItems = {}
        self.childNodeList = list(self.domNode)
    def node(self):
        #self.domNode = ET._Element("")
        return self.domNode
    def parent(self):
         #self.parentItem = ET._Element("")
        return self.parentItem
    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]
        if i >= 0 and i < len(self.domNode):
            childNode = self.childNodeList[i]
            childItem = DomItem(childNode,i, self)
            self.childItems[i] = childItem
            return childItem
        return None
    def row(self):
        return self.rowNumber


class PersistentStorageModel(QtCore.QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(PersistentStorageModel,self).__init__(parent)
        self.domDocument = document
        self.rootItem = DomItem(self.domDocument.getroot())
        self.logger = logging.getLogger("PersistentStorageModel")
    def columnCount(self, parent):
        return 3
    def data(self, index :QtCore.QModelIndex, role :QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        node = item.node()

        if index.column() == 0:
            return node.get('name')
        elif index.column() == 1:
            attrStr = []
            attributes = node.attrib
            for key,value in attributes.iteritems():
                attrStr.append(key + '="' + value + '"')
            return " ".join(attrStr)
        if index.column() == 2:
            value = node.text
            if value is None:
                return ''
            return ' '.join(value.split('\n'))
        return None
    def flags(self, index :QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def headerData(self, section, orientation, role :QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            if section == 1:
                return "Attributes"
            if section == 2:
                return "Value"
        return None    def index(self, row :int, column:int, parent=None):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
    def parent(self, child):
        if not child.isValid():
            return QtCore.QModelIndex()
        childItem = child.internalPointer()
        parentItem = childItem.parent()
        if not parentItem or parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)
    def rowCount(self, parent: QtCore.QModelIndex):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return len(parentItem.node())
    def setData(self,index = QtCore.QModelIndex(), value = "", role = QtCore.Qt.EditRole):
        if(role!=QtCore.Qt.EditRole):
            self.logger.info('setData failed')
            return False
        item = index.internalPointer()
        node = item.node();# node = ET._Element()
        column = index.column()
        if column != 2 :
            self.logger.debug('setData({0}) failed. Only allow changing text'.format(node.get('name')))
            return False #only allow changing text
        if(type(value) is not str):
            self.logger.debug('setData({0}) failed. value "{1}" is invalid'.format(node.get('name'), type(value)))
            return False
        '''
        psModel logic:
            user are not allowed to change psvn, psvnTilda, and softwareVersion
            psvnTilda = !psvn
            everytime press saveConfigToRemote--> softwareVersion ++
            (insert or delete rows) and (saveConfigToRemote) ll change psvn and psvnTilda as well
        '''
        if (node.get('name') == 'psvn') or (node.get('name') == 'psvnTilda') or (node.get('name') == 'softwareVersion'):
            self.logger.info('setData({0}) failed. User are not allowed to change psvn, psvnTilda, and softwareVersion'.format(node.get('name')))
            return False
        node.text = value
        self.logger.debug('setData successed')
        self.dataChanged.emit(index, index)
        return True         
    
        


'''
class PersistentStorageModel(QtCore.QAbstractItemModel):
    """Summary of class here.
    Attributes:
        @self.PSDom: xml.etree.ElementTree
    """
    def __init__(self, parent=None, xmlPath='./configurationDef.xml'):
        super(PersistentStorageModel, self).__init__(parent)
        self.PSDom = 0
        self.logger = logging.getLogger("PersistentStorageModel")
        self.itemList = list()
    def LoadConfigDomFromLocal(self, xmlPath='./python/configurationDef.xml'):
        try:
            self.PSDom = ET.parse(xmlPath)
        except Exception as e:
            self.logger.exception("Config file path is invalid")
#    def createIndex(self,row:int, column:int, object = 0):
#       return super().createIndex(int, object)
    def index(self,row: int, column: int, parent=QtCore.QModelIndex()):
        #self.PSDom = ET._ElementTree()
        if(not parent.isValid()):
            parentNode = self.PSDom.getroot()
        elif(len(parent.internalPointer()) == 0):
            parentNode = self.PSDom.getroot()
        elif(len(parent.internalPointer()) > 0):
            parentNode = self.itemList[parent.internalPointer].parentNode
        if(parentNode is None):
            parentNode = self.PSDom.getroot()
        indexedChildNode = 0
        try:
            indexedChildNode = parentNode[row]
        except IndexError:
            return QtCore.QModelIndex()
        if(indexedChildNode is None):
            return QtCore.QModelIndex()
        else:
            psItem = PersistentStorageItem(row,column,indexedChildNode,parentNode)
            self.itemList.append(psItem)
            return self.createIndex(row,column)
    def parent(self, index=QtCore.QModelIndex()):
        if(not index.isValid()):
            indexNode = self.PSDom.getroot()
        elif(len(index.internalPointer()) == 0):
            indexNode = self.PSDom.getroot()
        elif(len(index.internalPointer()) > 0):
            indexNode = index.internalPointer().pop()
        if(indexNode is None):
            indexNode = self.PSDom.getroot()
        return indexNode.parentNode
    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        if(not role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant()  
        if not index.isValid():
            return QtCore.QVariant()          
        else:
            column = index.column()
            indexNode = self.PSDom.getroot().find(index.internalPointer())[0]
            indexNode = ET.Element(indexNode)

            if(column == 0):
                text = indexNode.tag
                return text
            elif(column == 1):
                text = indexNode.text
                return text                
            elif(column == 2):
                attributes = []
                attributesDict = dict(indexNode.attrib)
                for key,value in attributes:
                    attributes.append(key + '="' + attribute.value + '"')
                return " ".join(attributes)            
    def flags(self, index=QtCore.QModelIndex()):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable    
    def columnCount(self,parent=QtCore.QModelIndex()):
        return 1
    def rowCount(self,parent=QtCore.QModelIndex()):
        if(not parent.isValid()):
            parentNode = self.PSDom.getroot()
        else:
            #self.PSDom.getroot().find(parent.internalPointer())[0]
            parentNode = self.itemList.pop().parentNode
        length = len(parentNode)
        return length
'''