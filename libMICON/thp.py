import Domoticz

class thp(object):
    def __init__(self):
        self.temperatureValue = 0
        self.pressureValue = 0.
        self.humidityValue = 0.
        self.humidityStatus = 0.
        self.lightlevel = 0.
        
    def createDevices(self):
        self.sensor = Domoticz.Device(Name= 'thp',  Unit=10, TypeName = "Temp+Hum+Baro", Used = 1)
        self.sensor.Create()
        self.lux = Domoticz.Device(Name= 'luxometr',  Unit=11, TypeName = "Illumination", Used = 1)
        self.lux.Create()

                
    def restoreDevices(self,Devices):
        self.sensor = Devices[10]
        try:
            self.lux = Devices[11]
        except KeyError:
            self.lux = Domoticz.Device(Name= 'luxometr',  Unit=11, TypeName = "Illumination", Used = 1)
            self.lux.Create()
    def deleteDevices(self,Devices):
        self.restoreDevices(Devices)
        self.sensor.Delete()
        self.lux.Delete()
        
    def update(self,msg):
        self.temperatureValue =round(float(msg["Temperature"]),2)
        self.pressureValue = msg["Pressure"]
        self.humidityValue = msg["Humidity"]
        self.setHumidityStatus(self.humidityValue)
        self.lightlevel = msg["LightLevel"]
        self.updateDevice()

    def setHumidityStatus(self, humidity):
        if humidity < 30:
            self.humidityStatus = 2
        elif humidity < 35:
            self.humidityStatus = 0
        elif humidity < 45:
            self.humidityStatus = 1
        elif humidity < 50:
            self.humidityStatus = 0 
        else:
            self.humidityStatus = 3
            
    def updateValue(self):
        return str(self.temperatureValue)+";"+str(self.humidityValue)+";"+str(self.humidityStatus)+";"+str(self.pressureValue)+";0"

    def updateDevice(self):
        self.sensor.Update(0,self.updateValue())
        self.lux.Update(0,str(self.lightlevel))
        
    def setEnabled(self, flag):
       timeout  = 0 if flag else 1
       self.sensor.Update(nValue = 0, sValue = self.updateValue(), TimedOut = 0)
       
       
       