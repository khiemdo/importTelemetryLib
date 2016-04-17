from pytelemetry import Pytelemetry
from pytelemetry.transports.serialtransport import SerialTransport
import xmltodict
import json
from logging import getLogger

class SerialController(object):
    configXMLPath = './python/configurationDef.xml'
    persistantStorage = dict()
    def __init__(self):
        self.log_tr = getLogger('SerialController')
        self.log_tr.info("SerialController initialized.")
        self.transport  = SerialTransport() 
        self.tlm = Pytelemetry(self.transport)
            
    def ConnectSerialCOM(self,port,baurate):
        self.transport.connect({'port': port, 'baudrate': baurate})

    def LoadDefaultConfigsFromXML(self):
        with open(self.configXMLPath) as fh:
            input_dict = xmltodict.parse(fh.read())
            self.persistantStorage = json.loads(json.dumps(input_dict))
    
    def ProcessConfigurationMsg(self,topic,data):
        if(topic=='FactorySettings' or topic=='UserSettings'):
#try/ catch here
            self.persistantStorage['PersistentConfigStorage'][topic][resList[0]]=resList[1]            
            
    def RequestPersistantStorage(self):
        self.tlm.publish('Config','query','string')
        self.tlm.subcribe('Config',self.ProcessConfigurationMsg)
        return 0
    #scan serial port availabe
    #convert dict data to correct format
    def ConvertSettingsDataTypesAccToXML(self, obj):
        pass
    def ConvertSettingDataTypesToString(self, obj):
        pass
