import unittest
import SerialController
from PersistentStorageModel import DomItem, PersistentStorageModel
import lxml.etree as ET

class TestSerialController(unittest.TestCase):
    def setUp(self):
        self.serialController = SerialController()
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