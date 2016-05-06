import unittest
from SerialController import *
from PersistentStorageModel import DomItem, PersistentStorageModel
import lxml.etree as ET
import struct
import logging

import SerialController
from PersistentStorageModel import DomItem, PersistentStorageModel
import lxml.etree as ET

class TestSerialController(unittest.TestCase):
    def setUp(self):
        self.serialController = SerialController()
        
        #self.serialController.Connect(3,115200)
        psDom = ET.parse('./testConfig.xml')
        self.model = PersistentStorageModel(psDom)
        self.serialController.SetModel(self.model)
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
        structSize = struct.calcsize(formatStr)
        self.assertEqual(structSize,0)

        length = len(valueList)
        self.assertEqual(length,0)
	
        psvnFactorySetting = valueList[0]
        self.assertTrue(psvnFactorySetting)

if __name__ == '__main__':
    unittest.main()
        self.serialController.Connect(3,115200)
        psDom = ET.parse('./python/testConfig.xml')
        self.model = PersistentStorageModel(psDom)
        self.logger = logging.getLogger("TestSerialController")

    def testGetPSFormatString(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def testGetPSValueList(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def testComposeFormatStringForCStructure(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
