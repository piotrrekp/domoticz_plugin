import Domoticz

class energyMeasure(object):
    def __init__(self):
        self.phaseValue = 0
        self.energyValue = 0.
        self.currentValue = 0.
        self.voltageValue = 0
        
    def createDevices(self):
        self.energy = Domoticz.Device(Name = 'Energy',  Unit=10, TypeName = "kWh", Used=1)  
        self.voltage = Domoticz.Device(Name = 'Voltage',  Unit=11, TypeName = "Voltage", Used=1)
        self.current = Domoticz.Device(Name = 'Current',  Unit=12, TypeName = "Current (Single)", Used=1)
        self.phase = Domoticz.Device(Name = 'Phase Shift',Unit=13, TypeName = "Custom")
        
        self.energy.Create() 
        self.voltage.Create() 
        self.current.Create() 
        self.phase.Create() 
        
    def restoreDevices(self,Devices):
        try:
            self.energy = Devices[10]
            self.voltage = Devices[11]
            self.current = Devices[12]
            self.phase = Devices[13]
            _ , self.energyValue = map(float,self.energy.sValue.split(";"))
        except KeyError:
            self.createDevices()
    def deleteDevices(self,Devices):
        self.restoreDevices(Devices)
        self.energy.Delete() 
        self.voltage.Delete() 
        self.current.Delete() 
        self.phase.Delete() 
       
    def update(self,msg):
        power,energy= msg['Power'],msg["Energy"]
        self.updateEnergy(power,energy)
        voltage = msg["Voltage"]
        self.updateVoltage(voltage)
        current =  msg["Current"]
        self.updateCurrent(current)
        phase = msg["Phase"]
        self.updatePhase(phase)
        
    def updateEnergy(self,power,energy):
        self.energyValue += float(energy)
        self.energy.Update(0, str(power)+";"+str(self.energyValue)) 
    def updateVoltage(self,voltage):
        self.voltageValue = round(voltage,1)  
        self.voltage.Update(0, str(self.voltageValue))
        
    def updateCurrent(self,current):
        self.currentValue = round(current,3)
        self.current.Update(0, str(self.currentValue))
   
    def updatePhase(self, phase):
        self.phaseValue = round(phase, 0)
        self.phase.Update(0, str(self.phaseValue))
        
        
        
        
        
        