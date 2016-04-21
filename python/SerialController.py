from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import xmltodict
import json
from logging import getLogger
from PersistentStorageModel import DomItem, PersistentStorageModel
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
    def ComposeFormatStringForCStructure(self):
        psFormatString=""
        psValuesList=[]
        root = self.model.rootItem.node()
        psFormatString,psValuesList=self.FormatStringNValueConstructor(root)
        self.logger.info("psFormatStringRet:{0}".format(psFormatString))
        self.logger.info("psValuesList:{0}".format(psValuesList))
    def FormatStringNValueConstructor(self,node):
        nodeLength = len(node)
        if (nodeLength==0):
            stringRet=""
            valueListRet = []
            try:
                nodeType = node.get('type')
                nodeLength = node.get('length')
                try: 
                    typeStr,value = self.ConvertValueType_wrt_FormatString(nodeType,node.text, nodeLength)
                except Exception as e:
                    raise Exception('illed format psXML')
                valueListRet.extend([value])
                stringRet = typeStr  
            except Exception as e:
                self.logger.exception("got error, set string ret = """)
                stringRet = ""      
            finally:            
                return (stringRet, valueListRet)
        elif (nodeLength>0):
            stringRet=""
            valueListRet = []
            for formatStr, valueList in map(self.FormatStringNValueConstructor,node.iterchildren()):
                stringRet += (formatStr + " ")
                valueListRet.extend(valueList)
            return (stringRet, valueListRet)
    def ConvertValueType_wrt_FormatString(self,nodeType,text, length = None):
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

    def ConnectSerialCOM(self,port,baurate):
        self.transport.connect({'port': port, 'baudrate': baurate})
    def SetModel(self,model):
        self.model = model
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
    def TransferPersistentStorage(self):
        rootNode = self.model.rootItem.node()
        factoryNode = self.model.GetFactorySettingItem().node()
        userSettingNode = self.model.GetUserSettingsItem().node()
        for element in factoryNode.iter(tag=etree.Element):
            topic = element.get('name')
            self.tlm.publish("F"+ topic,topic.text)
    #scan serial port availabe
    #convert dict data to correct format
    def ConvertSettingsDataTypesAccToXML(self, obj):
        pass
    def ConvertSettingDataTypesToString(self, obj):
        pass
