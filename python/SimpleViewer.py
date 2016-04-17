import sys
from pprint import pprint

class SimpleViewer(object):
    """description of class"""
    def __init__(self):
        self.flag = 0
    def DisplayDict(self,obj):
        #pprint(obj, indent=4)
        print(json.dumps(obj, indent=4))
    def GUIDisplayDict(self,obj):
        return 0