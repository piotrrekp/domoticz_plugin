"""
<plugin key="mic3" name="mic3" author="piotrrek" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://www.micon.pl/">
    <params>
       <param field="Mode1" label="Timeout" width="75px" required="true">
            <options>
                <option label="30 seconds" value="0.5"/>
                <option label="1 minute" value="1.0"default="true" />
                <option label="2 minutes" value="2.0"/>
                <option label="5 minutes" value="5.0"/>
                <option label="10 minutes" value="10.0"/>
            </options> 
        </param>
    </params>
</plugin>
"""

import os
import json
import time
import datetime
import Domoticz

from libMICON.utility import *
from libMICON.modules import *
from libMICON.testy import *


FIRST_CONNECTION_SENDING_PORT = 17666
FIRST_CONNECTION_RECIVING_PORT= 17667
BASE_PORT = 60000

CONFIG_COMPLETE = "module ready to use"
REMOVE_DEVICE = "unmount device"
FIRST_TIME = "first time"
NEW_MAC = "new mac"


class BasePlugin:
    def __init__(self):
        return
    def onStop(self): 
        self.locker.relase()
    def onStart(self):
        self.ipAddress = ""
        self.status = "empty status"
        self.id = Parameters["HardwareID"]
        self.sender = None
        self.reciver = None
        self.sendingport = BASE_PORT + self.id * 2
        self.recivingport = BASE_PORT + self.id *2 + 1
        self.homeFolder = Parameters["HomeFolder"]
        self.deviceName = Parameters["Name"]
        self.timeout = float(Parameters["Mode1"])
        self.gotoConfigDir()
        self.path = os.getcwd()
        self.locker = locky(str(self.id))
        self.locker.relase()
        self.handle_module_config()
        if self.status == CONFIG_COMPLETE:
            self.init_module()
            self.init_connection()
            Domoticz.Heartbeat(10)
           
        else:
            Domoticz.Heartbeat(5)
        

    def gotoConfigDir(self):
        os.chdir(self.homeFolder)
        log(os.getcwd())
        if not os.path.isdir("config"):
            os.makedirs("config")
        os.chdir("config")
        
    def handle_module_config(self):
        self.allcfg = TotalConfig(self.path)
        self.config = config(self.path,self.id)
        if not self.allcfg.hardwareid_is_stored(self.id):
            self.status = FIRST_TIME
        else:
            module = self.allcfg.get_line_with_hid(self.id)
            _, _, _, plugintype , _ = module
            self.type = plugintype
            self.config.set_config(module)
            self.config.write()
            self.status = CONFIG_COMPLETE

    def init_module(self):
        creator = Module()
        if self.status == CONFIG_COMPLETE:
            self.dev = creator.create(self.type)
            if len(Devices) == 0:
                self.dev.createDevices()
            else:
                self.dev.restoreDevices(Devices)
            try:
                self.removeButton = Devices[21]
            except KeyError:
                self.removeButton = Domoticz.Device(Name="status",Unit=21, Type=244, Subtype=73, Switchtype=0, Used=0,Image=9)
                self.removeButton.Create()
        elif self.status == CHANGE_PLUGIN_TYPE:
            log(len(Devices))
            self.dev = creator.create(self.config.get_type())
            self.dev.deleteDevices(Devices)
            self.status = CONFIG_COMPLETE
            self.config.set_plugin_type(self.type)
            self.config.write()
            module = self.config.get_config()
            self.allcfg.update_module(self.id, module)
            self.init_module()

    def init_connection(self):
        log("inicjalizacja polaczen")
        self.reciver = Domoticz.Connection(Name="reciver", Transport="UDP/IP", Protocol="None", Address="127.0.0.1", Port=str(self.sendingport))
        self.reciver.Listen()
        log(self.reciver)
        self.sender = Domoticz.Connection(Name="sender", Transport="UDP/IP", Protocol="JSON", Address = self.config.get_ip(), Port=str(self.recivingport))
        log(self.sender)
        Domoticz.Heartbeat(30)
        
    def onMessage(self, Connection, Data, Status, Extra):
        msg  = json.loads(Data.decode())
        log(msg)
        Devices[21].Update(1,"On")
        if msg["Type"] == "RestartRequest":
            self.reciver.Disconnect()
#             self.sender.Disconnect()
            self.init_connection()
        elif msg["Type"] == "PeriodicRaport" and msg["IP"] != self.config.get_ip():
            self.config.set_ip(msg["IP"])
            self.config.write()
            self.sender = Domoticz.Connection(Name="sender", Transport="UDP/IP", Protocol="JSON", Address = self.config.get_ip(), Port=str(self.recivingport))
        elif msg["Type"] == "Confirm":
            msg["Type"] = "Change"
        elif msg["Type"] == "DeviceRemoved":
            log(msg)
            self.dev.deleteDevices(Devices)
            self.config.remove()
            self.allcfg.remove_module(self.id)
            Devices[21].Delete()
            self.reciver.Disconnect()
            self.onStart()
        self.dev.handleMessage(msg)

    def onCommand(self, Unit, Command, Level, Hue):
        if Unit == 21:
            self.sender.Send("{Type: RemoveDevice}")
        else:
            self.toSend = self.dev.handleCommand(Unit, Command)
            self.sender.Send(dictToString(self.toSend))
        
            
    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)
    
    def onDisconnect(self, Connection):
        pass
    
    def onHeartbeat(self):
        if self.locker.isLock():
            msg = self.prepareMessage()
            log(msg)
            BroadcastMessage(msg, FIRST_CONNECTION_SENDING_PORT)
            try:
                recivingmessage, self.ipAddress = CatchMessage(FIRST_CONNECTION_RECIVING_PORT)
            except:
                recivingmessage = ""
                self.ipAddress = ""
            log(recivingmessage)
            self.handleMessage(recivingmessage)
            if self.status == CONFIG_COMPLETE:
                self.locker.relase()
                self.handle_module_config()
                self.init_module()
                self.init_connection()
        elif self.locker.anyLockFileExist() and self.status != CONFIG_COMPLETE:
                log("Waiting for my queue")
        else:
            if self.status != CONFIG_COMPLETE:
                self.locker.lock()
            else:
                if isDevicesOnline(self.reciver.LastSeen(),self.timeout):
                    Devices[21].Update(1,"On")
                else:
                    Devices[21].Update(0,"Off")
    def prepareMessage(self):
        msg = {
            "IP": getLocalIP(),
            "PortNadawczy" : self.recivingport,
            "PortOdbiorczy": self.sendingport
            }
        if self.status == FIRST_TIME:
            msg["Type"] = "WelcomeMessage"
            msg["MAC"] = ""
        elif self.status == NEW_MAC:
            msg["Type"] = "WelcomeMessage"
            msg["MAC"] = self.config.get_mac()
            log("new_mac: %s"  % self.config.get_mac())
        elif self.status == CONFIG_COMPLETE:
            msg["Type"] = "HeartbeatWelcome"
            msg["MAC"] = self.config.get_mac()
        elif self.status == REMOVE_DEVICE:
            msg["Type"] = "RemoveDevice"
            msg["MAC"] = self.config.get_mac()
        else:
            raise ValueError()
        return dictToString(msg)
     
    def handleMessage(self, msg):
        try:
            log(msg)
            message = json.loads(msg.decode())
            type = message["Type"]
            if type == "FirstMessage":
                self.checkMac(message["MAC"])
            elif type == "Ok":
                log(self.id)
                log(message["MAC"])
                log(self.ipAddress)
                log(message["Module"])
                
                newmodule = (str(self.id), message["MAC"], self.ipAddress, message["Module"], message["Module"])

                self.config.set_config(newmodule)
                self.config.write()
                self.allcfg.write(newmodule)
                self.status = CONFIG_COMPLETE
                self.locker.relase()
            else:
                log("UNHANDLED TYPE: %s" %type)
        except: 
            pass
        
    def checkMac(self, mac):
        if not self.allcfg.mac_is_stored(mac):
            self.config.set_mac(mac)
            self.status = NEW_MAC  
        elif self.allcfg.mac_is_stored(mac):
            newmodule = self.allcfg.get_line_with_mac(mac)
            hid,self.mac,self.ipAddress,_,_ = newmodule
            if hid == str(self.id):
                self.config = config(os.getcwd(), self.id)
                self.config.set_config(newmodule)
                self.config.write()
                self.status = CONFIG_COMPLETE
            else:
                pass




global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onMessage( Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data, Status="", Extra="")

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return



