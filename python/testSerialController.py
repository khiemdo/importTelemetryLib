import unittest
from SerialController import *
from PersistentStorageModel import DomItem, PersistentStorageModel
import lxml.etree as ET
import struct
import logging

class TestSerialController(unittest.TestCase):
    def setUp(self):
        self.serialController = SerialController()
        #self.serialController.Connect(3,115200)
        psDom = ET.parse('./testConfig.xml')
        self.model = PersistentStorageModel(psDom)
        self.logger = logging.getLogger("TestSerialController")

       

    def testGetPSFormatString(self):
        formatStr = self.serialController.GetPSFormatString()
        structSize = struct.calcsize(formatStr)
        self.assertEqual(structSize, 0)

    def testGetPSValueList(self):
        valueList = self.serialController.GetPSValueList()
        length = len(valueList)
        self.assertTrue(length, 0)
        psvnFactorySetting = valueList[0]
        self.assertTrue(psvnFactorySetting,0) 

    def testComposeFormatStringForCStructure(self):
        formatStr, valueList = self.serialController.ComposeFormatStringForCStructure()
        structSize = struct.calsize(formatStr)
        self.assertEqual(structSize,0)

        length = len(valueList)
        self.assertEqual(length,0)
	
        psvnFactorySetting = valueList[0]
        self.assertTrue(psvnFactorySetting)

if __name__ == '__main__':
    unittest.main()
