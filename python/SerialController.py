from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import xmltodict
import json
from logging import getLogger
from PersistentStorageModel import DomItem, PersistentStorageModel
import struct


class SerialController(object):
    FORMAT_STRING_ENCODE = {
	                         'char':'c',
	                         'char[]':'s',
	                         'void*':'P',
	                         'uint8_t':'B',
	                         'int8_t':'b',
	                         'uint16_t':'H',
	                         'int16_t':'h',
	                         'uint32_t':'I',
	                         'int32_t':'i',
	                         'float_t':'f',
	                         'signed int':'I',
	                         'unsigned int':'i',
	                         'unsigned long':'L',
	                         'signed long':'l',
	                         'float':'f',
	                         'double':'d'}
    def __init__(self):
        self.logger = getLogger('SerialController')
        self.logger.info("SerialController initialized.")
        self.transport  = SerialTransport() 
        self.tlm = Pytelemetry(self.transport)    
        self.model = None
        #self.cStructWorker = struct.Struct(self.GetPSFormatString())

    def GetPSFormatString(self, createFlag = 0):
        if createFlag!=0 or self.psFormatString is None:
            root = self.model.rootItem.node()
            self.psFormatString = self.__PSFormatString_PSValue_Constructor(root,1)
        return self.psFormatString
    def GetPSValueList(self,createFlag=0):
        if createFlag!=0 or self.psValueList is None:
            root = self.model.rootItem.node()
            self.psValueList = self.__PSFormatString_PSValue_Constructor(root,2)
        return self.psValueList        
    def ComposeFormatStringForCStructure(self):
        psFormatString=""
        psValuesList=[]
        root = self.model.rootItem.node()
        psFormatString,psValuesList=self.__PSFormatString_PSValue_Constructor(root)
        self.logger.info("psFormatStringRet:{0}".format(psFormatString))
        self.logger.info("psValuesList:{0}".format(psValuesList))
    '''
        retOption = 0--> return both formatstring and valuelist
        retOption = 1--> return formatstring
        retOption = 2--> return valuelist
    '''
    def __PSFormatString_PSValue_Constructor(self,node,retOption=0):
        nodeLength = len(node)
        if (nodeLength==0):
            stringRet=""
            valueListRet = []
            try:
                nodeType = node.get('type')
                nodeLength = node.get('length')
                try: 
                    typeStr,value = self.GenerateFormatStringNValueFromNode(nodeType,node.text, nodeLength)
                except Exception as e:
                    raise Exception('illed format psXML')
                if(retOption==0):
                    valueListRet.extend([value])
                    stringRet = typeStr  
                elif (retOption==1):
                    stringRet = typeStr 
                elif (retOption==2):
                    valueListRet.extend([value])
            except Exception as e:
                self.logger.exception("got error, set string ret = """)
                stringRet = ""    
        elif (nodeLength>0):
            stringRet=""
            valueListRet = []
            for child in node.iterchildren():
                if(retOption==0):
                    formatStr, valueList = self.__PSFormatString_PSValue_Constructor(child,retOption)
                    stringRet += (formatStr + " ")
                    valueListRet.extend(valueList)
                elif (retOption==1):
                    formatStr = self.__PSFormatString_PSValue_Constructor(child,retOption)
                    stringRet += (formatStr + " ")
                elif (retOption==2):
                    valueList = self.__PSFormatString_PSValue_Constructor(child,retOption)
                    valueListRet.extend(valueList)
        if(retOption==0):
            return (stringRet, valueListRet)
        elif (retOption==1):
            return (stringRet)
        elif (retOption==2):
            return (valueListRet)
    def GenerateFormatStringNValueFromNode(self,nodeType,text, length = None):
        ret = 0
        if(nodeType == "uint8_t" or 
            nodeType == "int8_t" or 
            nodeType == "uint16_t" or 
            nodeType == "int16_t" or 
            nodeType == "uint32_t" or 
            nodeType == "int32_t" ):
            if(text is None):
                ret = (SerialController.FORMAT_STRING_ENCODE[nodeType], 0)
            else:
                ret = (SerialController.FORMAT_STRING_ENCODE[nodeType], int(text,0))
            return ret
        elif (nodeType == "float_t"): 
            if(text is None):
                ret = (SerialController.FORMAT_STRING_ENCODE[nodeType], 0.0)
            else:
                ret = (SerialController.FORMAT_STRING_ENCODE[nodeType], float(text))
        elif (nodeType == "char"):
            if(text is None):
                ret = (SerialController.FORMAT_STRING_ENCODE[nodeType], "")
            else:
                ret = (SerialController.FORMAT_STRING_ENCODE[nodeType], text.encode("ascii") ) 
        elif(nodeType == "char[]"):
            if(text is None):
                ret = ("0"+ SerialController.FORMAT_STRING_ENCODE[nodeType], "")
            else:
                ret = (str(length)+ SerialController.FORMAT_STRING_ENCODE[nodeType], text.encode("ascii"))
        return ret   

    def SendPersistentStorageCStruct(self):
        psValueList = self.GetPSValueList(1)
        self.tlm.publish("PersistentStorage",self.cStructWorker.pack(*psValueList),"int32")

    def Connect(self,port,baurate=115200):
        self.transport.connect({'port': port, 'baudrate': baurate})
    def SetModel(self,model):
        self.model = model
    def RequestPersistentStorage(self):
        self.tlm.publish('PersistentStorage','query','string')
        self.tlm.subscribe('PersistentStorage',self.PersistentStorageMsgHandle)
    def PersistentStorageRcvMsgHandle(self,topic,data):
        unpacked_data = self.cStructWorker.unpack(data)
        self.logger.info(unpacked_data)
        root = self.model.rootItem.node()
        self.AssignValuesIntoParentNode(root,unpacked_data,0)

    def AssignValuesIntoParentNode(self, node, data,index = 0):
        nodeLength = len(node)
        if (nodeLength==0):
            value = data[index]
            index+=1
            self.__AssignValueToLeafNode(node,value)
        elif (nodeLength>0):
            for child in node.iterchildren():
                self.__AssignValuesIntoParentNode(child,data,index)
        return index
    def AssignValueToLeafNode(self,node,value):
        nodeType = node.get('type')
        nodeLength = node.get('length')
        if nodeType is None or nodeLength is None:
            raise Exception ("illed format psXML")
            return
        if(nodeType == "uint8_t" or 
            nodeType == "int8_t" or 
            nodeType == "uint16_t" or 
            nodeType == "int16_t" or 
            nodeType == "uint32_t" or 
            nodeType == "int32_t" ):
            if(value is None):
                node.text = str(0)
            else:
                node.text = str(value)
        elif (nodeType == "float_t"): 
            if(value is None):
                node.text = str(0.0)
            else:
                node.text = str(value)
        elif (nodeType == "char"):
            if(value is None):
                node.text = ""
            else:
                node.text = unicode(value)
        elif(nodeType == "char[]"):
            if(value is None):
                node.text = ""
            else:
                node.text = unicode(value)
        self.logger.info("nodeName {0}, the type of which is {1}, s assigned value {2}", unicode(value))
'''
    def RequestPersistantStorage(self):
        self.tlm.publish('PersistentStorage','query','string')
        self.tlm.subscribe(None,self.PersistentStorageTransferEnd)
        self.tlm.subscribe('PersistentStorageTransferEnd',self.TerminaSubscribePersistentStorageMsg)
    def ProcessPersistentStorageTransferMsg(self,topic,data): 
        #self.model = PersistentStorageModel(None)
        if(self.model is None):
            return False
        self.logger.info("process topic {0}".format(topic))
        rootNode = self.model.rootItem.node()
        nameLookupList = topic.split("/")
        xpathString = "."
        for nameLookup in nameLookupList:
            xpathString += "/item[@name='{0}']".format(nameLookup)
        self.logger.info("xpath={0}".format(xpathString))

        try:
            node = rootNode.find(xpathString)
        except Exception as e:
            self.logger.exception("cannot find with xpath {0}".format(xpathString))
            return False
        if node is None:
            return False
        else:
            node.text = data
    def TerminaSubscribePersistentStorageMsg(self,topic,data): 
        self.tlm.subscribe(None,None)
'''
