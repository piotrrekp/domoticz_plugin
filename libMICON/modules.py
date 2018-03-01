import Domoticz
from libMICON.energyClass import *
from libMICON.output import *
from libMICON.thp import *


class Module(object):
    def create(self,type):
        if type == "M1W":
            return ModuleSimpleOutput(1)
        elif type == "M2W":
            return  ModuleSimpleOutput(2)
        elif type == "M1E":
            return ModuleE(1)
        elif type == "M2E":
            return ModuleE(2)
        elif type == "B1W":
            return ModuleBistable(1)
        elif type == "B2W":
            return ModuleBistable(2)
        elif type == "B1E":
            return ModuleBistableWithEnergyMeasure(1)
        elif type == "B2E":
            return ModuleBistableWithEnergyMeasure(2)
        elif type == "THP":
            return ModuleTHP()
    
        
class ModuleE(object):
    def __init__(self,nOutputs):
        if nOutputs == 2:
            self.output = doubleSimpleOutput()
        elif nOutputs == 1:
            self.output = singleSimpleOutput()
        self.addition = energyMeasure()
        
    def createDevices(self):
        self.output.createDevices()
        self.addition.createDevices()
        
    def restoreDevices(self,Devices):
        self.output.restoreDevices(Devices)
        self.addition.restoreDevices(Devices)

    def deleteDevices(self,Devices):
        self.output.deleteDevices(Devices)  
        self.addition.deleteDevices(Devices)
        
    def handleCommand(self, Unit,Command):
        if Unit < 10:
            return self.output.handleCommand(Unit,Command)
        elif Unit < 20:
            return self.addition.handleCommand(Unit,Command)
            
    def handleMessage(self,msg):
        if msg["Type"] == "PeriodicRaport":
            self.addition.update(msg)
            self.output.update(msg)
        elif msg["Type"] == "Change" or msg["Type"] == "RestartRequest":
            self.output.update(msg)
        else:
            print("UNHANDLED MESSAGE:")
            print(msg)

class ModuleBistable(object):
    def __init__(self,nOutputs):
        if nOutputs == 2:
            self.output = doubleBistableOutput()
        elif nOutputs == 1:
            self.output = singleBistableOutput()
            
    def createDevices(self):
        self.output.createDevices()
    
    def restoreDevices(self,Devices):
        self.output.restoreDevices(Devices)
    
    def deleteDevices(self,Devices):
        self.output.deleteDevices(Devices)  

    def handleCommand(self, Unit,Command):
        if Unit < 10:
            return self.output.handleCommand(Unit,Command)
    
    def handleMessage(self,msg):
        if msg["Type"] == "Change" or msg["Type"] == "RestartRequest" or msg["Type"] == "PeriodicRaport":
            self.output.update(msg)
        else:
            print("UNHANDLED MESSAGE:")
            print(msg)

class ModuleBistableWithEnergyMeasure(object):
    def __init__(self,nOutputs):
        if nOutputs == 2:
            self.output = doubleBistableOutput()
        elif nOutputs == 1:
            self.output = singleBistableOutput()
        self.addition = energyMeasure()
        
    def createDevices(self):
        self.output.createDevices()
        self.addition.createDevices()

    def restoreDevices(self,Devices):
        self.output.restoreDevices(Devices)
        self.addition.restoreDevices(Devices)
        
    def deleteDevices(self,Devices):
        self.output.deleteDevices(Devices)  
        self.addition.deleteDevices(Devices)
    
    def handleCommand(self, Unit,Command):
        if Unit < 10:
            return self.output.handleCommand(Unit,Command)
            
    def handleMessage(self,msg):
        if msg["Type"] == "RestartRequest":
            self.output.update(msg)
        elif msg["Type"] == "PeriodicRaport":
            self.output.update(msg)
            self.addition.update(msg)
        elif msg["Type"] == "Change":
            self.output.update(msg)
        else:
            print("UNHANDLED MESSAGE:")
            print(msg)
            
class ModuleTHP(object):
    def __init__(self):
        self.addition = thp()
        
    def createDevices(self):
        self.addition.createDevices()
    
    def restoreDevices(self,Devices):
        self.addition.restoreDevices(Devices)
    
    def deleteDevices(self,Devices):
        self.addition.deleteDevices(Devices)
        
    def handleCommand(self, Unit,Command):
        pass
    def handleMessage(self,msg):
        if msg["Type"] == "PeriodicRaport":
            self.addition.update(msg)
    def LastUpdate(self):
        return self.addition.sensor.LastUpdate
    def setEnabled(self,flag):
        self.addition.setEnabled(flag)
        
class ModuleSimpleOutput(object):
    def __init__(self,nOutputs):
        if nOutputs == 2:
            self.output = doubleSimpleOutput()
        elif nOutputs == 1:
            self.output = singleSimpleOutput()
            
    def createDevices(self):
        self.output.createDevices()
    
    def restoreDevices(self,Devices):
        self.output.restoreDevices(Devices)
    
    def deleteDevices(self,Devices):
        self.output.deleteDevices(Devices)
        
    def handleCommand(self, Unit,Command):
        if Unit < 10:
            return self.output.handleCommand(Unit,Command)
    
    def handleMessage(self,msg):
        if msg["Type"] == "Change" or msg["Type"] == "RestartRequest" or msg["Type"] == "PeriodicRaport":
            self.output.update(msg)
        else:
            print("UNHANDLED MESSAGE:")
            print(msg)

    def lastSeen(self):
        return self.output.lastSeen()
    
    def setOffline(self):
        self.output.setOffline()

class newModule(object):
    def __init__(self):
        pass
    def createDevices(self):
        pass
    def restoreDevices(self, Devices):
        pass
    def deleteDevices(self, Devices):
        pass
    def handleCommand(self, Unit,Command):
        pass
    def handleMessage(self,msg):
        pass
