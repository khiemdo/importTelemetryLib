import sys
import os

# os.path.dirname(os.path.realpath(__file__))
sys.path.append("./python")
from SimpleViewer import SimpleViewer
from SerialController import SerialController
'''
with open("startup.py") as f:
    code = compile(f.read(), "startup.py", 'exec')
    exec(code)

with open("./python/pyqtExample1.py") as f:
    code = compile(f.read(), "./python/pyqtExample1.py", 'exec')
    exec(code)

PSDom=ET.parse('./python/configurationDef.xml')
root = PSDom.getroot()
factorySettings = root.findall("FactorySettings")
psvn = factorySettings[0].findall("./item[1]")[0]


'''
