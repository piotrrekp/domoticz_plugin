import Domoticz
from . import utility
class singleSimpleOutput(object):
    def __init__(self):
        self.out1Value = 0
        
    def createDevices(self):        
        self.out1 = Domoticz.Device(Name = 'Out1',  Unit=1, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.out1.Create()
    
    def restoreDevices(self,Devices):
        self.out1 = Devices[1]
            
    def deleteDevices(self,Devices):
        self.restoreDevices(Devices)
        self.out1.Delete()
        
    def update(self, msg):
        self.out1Value = msg["Out1"]
        self.updateOutput(self.out1Value)

    def getStringValue(self, value):
        if value == 1: return "On"
        else: return "Off"
        
    def updateOutput(self, out1 = -1):
        self.out1.Update(self.out1Value, self.getStringValue(self.out1Value))
  
    def handleCommand(self, Unit,Command):
        if str(Command) == "On": value = 1
        else: value = 0
        if Unit == 1: 
            if value != self.out1Value:
#                 self.updateOutput(out1 = value)
                self.out1Value = value
                handle =  {
                    "Type" : "Change",
                    "Out1" : self.out1Value,
                    }
            else: handle = {}
        return handle
class doubleSimpleOutput(object):
    def __init__(self):
        self.out1Value = 0
        self.out2Value = 0

    def createDevices(self):        
        self.out1 = Domoticz.Device(Name = 'Out1',  Unit=1, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.out2 = Domoticz.Device(Name = 'Out2',  Unit=2, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.out1.Create()
        self.out2.Create()
        
    def restoreDevices(self,Devices):
        try:
            self.out1 = Devices[1]
            self.out2 = Devices[2]
        except KeyError:
            self.createDevices()
            
    def deleteDevices(self,Devices):
        self.restoreDevices(Devices)
        self.out1.Delete()
        self.out2.Delete()
        
    def update(self, msg):
        self.out1Value = msg["Out1"]
        self.out2Value = msg["Out2"]
        self.updateOutput()
        
    def getStringValue(self, value):
        if value == 1: return "On"
        else: return "Off" 
    
    def updateOutput(self):
        self.out1.Update(self.out1Value, self.getStringValue(self.out1Value))
        self.out2.Update(self.out2Value, self.getStringValue(self.out2Value))
    
    def handleCommand(self,Unit,Command):
        if str(Command) == "On": value = 1
        else: value = 0
        if Unit == 1: 
            if value != self.out1Value:
                self.out1Value = value
                handle = {
                    "Type" : "Change",
                    "Out1" : self.out1Value,
                    "Out2" : self.out2Value
                    }
            else: handle = {}
        if Unit == 2: 
            if value != self.out2Value:
                self.out2Value = value
                handle = {
                    "Type" : "Change",
                    "Out1" : self.out1Value,
                    "Out2" : self.out2Value
                }
            else: handle = {}
        return  handle
    
    
class doubleBistableOutput(object):
    def __init__(self):
        self.out1Value = 0
        self.out2Value = 0
        self.in1Value = 0
        self.in2Value = 0
        
    def createDevices(self):        
        self.out1 = Domoticz.Device(Name = 'Out1',  Unit=1, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.out2 = Domoticz.Device(Name = 'Out2',  Unit=3, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.in1  = Domoticz.Device(Name = 'In1',  Unit=2, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.in2  = Domoticz.Device(Name = 'In2',  Unit=4, Type=244, Subtype=73, Switchtype=0, Used=1)
        
        self.out1.Create()
        self.out2.Create()
        self.in1.Create()
        self.in2.Create()
        
    def restoreDevices(self,Devices):
        try:
            self.out1 = Devices[1]
            self.out2 = Devices[3]
            self.in1  = Devices[2]
            self.in2  = Devices[4]
            
        except KeyError:
            self.createDevices()        

    def deleteDevices(self,Devices):
        self.restoreDevices(Devices)
        self.out1.Delete()
        self.out2.Delete()
        self.in1.Delete()
        self.in2.Delete()
        
    def update(self, msg): 
        self.in1Value = msg["In1"]
        self.in2Value = msg["In2"]
        self.out1Value = msg["Out1"]
        self.out2Value = msg["Out2"]
        self.updateOutput()
        self.updateInput()
        
    def getStringValue(self, value):
        if value == 1: return "On"
        else: return "Off" 
          
    def updateOutput(self):
            self.out1.Update(self.out1Value, self.getStringValue(self.out1Value))
            self.out2.Update(self.out2Value, self.getStringValue(self.out2Value))
            
    def updateInput(self):
        self.in1.Update(self.in1Value, self.getStringValue(self.in1Value))
        self.in2.Update(self.in2Value, self.getStringValue(self.in2Value))
    
    def handleCommand(self,Unit,Command):
        utility.log(Unit)
        utility.log(Command)
        
        if str(Command) == "On": value = 1
        else: value = 0
        if Unit == 1 :
            if value !=  self.out1Value: 
                self.out1Value = value
                handle = {
                    "Type" : "Change",
                    "Out1" : self.out1Value,
                    "Out2" : self.out2Value
                }
            else:
                handle = {} 
        elif Unit == 3 : 
            if value != self.out2Value:
                self.out2Value = value
                handle = {
                    "Type" : "Change",
                    "Out1" : self.out1Value,
                    "Out2" : self.out2Value
                }
            else:
                handle = {}
    
        else:
            handle = {}
        return handle 

class singleBistableOutput(object):
    def __init__(self):
        self.out1Value = 0
        self.in1Value = 0

    def createDevices(self):        
        self.out1 = Domoticz.Device(Name = 'Out1',  Unit=1, Type=244, Subtype=73, Switchtype=0, Used=1)
        self.in1  = Domoticz.Device(Name = 'In1',  Unit=2, Type=244, Subtype=73, Switchtype=0, Used=1)
        
        self.out1.Create()
        self.in1.Create()
        
    def restoreDevices(self,Devices):
        try:
            self.out1 = Devices[1]
            self.in1  = Devices[2]
        except KeyError:
            self.createDevices()        
    def deleteDevices(self,Devices):
        self.restoreDevices(Devices)
        self.out1.Delete()
        self.in1.Delete()
            
    def update(self, msg):
        self.in1Value = msg["In1"]
        self.updateInput()
        if msg["Type"] == "RestartRequest":
            self.out1Value = msg["Out1"]
        self.updateOutput()
        
    def getStringValue(self, value):
        if value == 1: return "On"
        else: return "Off" 
    
    def updateOutput(self):
        self.out1.Update(self.out1Value, self.getStringValue(self.out1Value))

    def updateInput(self):
        self.in1.Update(self.in1Value, self.getStringValue(self.in1Value))
    
    def handleCommand(self,Unit,Command):
        if Unit == 1 :
            if str(Command) == "On": value = 1
            else: value = 0
            if value != self.out1Value:
                self.out1Value = value
                handle = {
                    "Type" : "Change",
                    "Out1" : self.out1Value,
                }
            else: handle = {}
        else:
            handle = {}
        return handle
