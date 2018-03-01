import os
from socket import *
import string
import time
import datetime
import json
import Domoticz
from datetime import date

class locky(object):
    def __init__(self, name):
        self.name = name
        self.extension = "lock"
        self.filename = self.name + "." + self.extension
        
    def lock(self):
        if not self.anyLockFileExist():
            f = open(self.filename, "w")
            f.close()
    
    def isLock(self):
        return os.path.isfile(self.filename)
    
    def relase(self):
        if self.isLock():
            fullpath = os.path.join(os.getcwd(),self.filename)
            os.remove(fullpath)
        else:
            return
        
    def anyLockFileExist(self):
        for file in os.listdir("."):
            ext  = file.split(".")[-1]
            if ext == self.extension:
                return True
        else: 
            return False
        
def isDevicesOnline(lastUpdate, timeout):
    #timeout in minutes
    y,mo,d,h,m,s = map(int,str(lastUpdate).replace('-', ' ').replace(':',' ').replace('.',' ').split(' '))
    last = datetime.datetime(y,mo,d,h,m,s)
    now = datetime.datetime.now()
    diff = now - last
    if diff.total_seconds() < timeout * 60:
        return True
    else:
        return False
    
def log(msg):
    Domoticz.Log(str(msg))

def saveConfigFile(data, filePath):
    with open(filePath, "a") as configFile:
        line = json.dumps(data)
        configFile.write(line)
        configFile.write("\n")

def readConfigFile(filePath):
    module = []
    try:
        with open(filePath, "r") as configFile:
            for line in configFile:
                print(line)
                module.append(json.loads(line))
    except:
        print("error while reading module list!")
    return module
def dictToString(data):
    print(data)
    message = "{"
    for k,v in data.items():
        vv = str(v)
        kk = str(k)
        message += "'" + kk + "':'" + vv + "',"
    mess = message[:-1]
    mess += "}"
    return mess

def getMac(macString):
    mac = ""
    macString.strip(" ")
    for i in macString.split(":"):
        mac+=i
    return mac

def updateMacFile(macTable, path):
    filename = path + "macList.cfg"
    log(macTable)
    try:
        macFile = open(filename, "w")
        for mac in macTable:
            macFile.write(mac)
        macFile.close()
    except IOError:
        log("Error while updating macList.cfg file!!!")
        
def getConfigFilePath(home, name):
    return home + "config/" + name + ".cfg"

def storeMacInFile(newMac, path):
    filename =path + "macList.cfg"
    if fileExist(filename):
        file = open(filename, "a")
    else:
        file = open(filename, "w")
    macList = file.readlines()
    if not newMac in macList:
        file.write(newMac)
    file.close()

def fileExist(fullPath):
    return os.path.exists(fullPath)

def getFullPathToConfigFile(pathToPlugin, deviceName):
    fullPath = pathToPlugin+deviceName+".cfg"
    return fullPath

def getTypeStoredModule(fullPath):
    f = open(fullPath, "r")
    moduleType = f.readline()
    return moduleType.strip(string.whitespace)

def getLocalIP():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('10.255.255.255',0))
        IP = s.getsockname()[0]
    except:
        getLocalIP()
    finally:
        s.close()
    return IP

def prepareIPforUPD(IP):
    octets =IP.split('.')
    octets[3] = 255
    udpIP = ".".join(map(str, octets))
    return udpIP

def UDPIncomingMessage(port):
    timeout = 0.3
    UDPip = getLocalIP()
    UDPport = int(port)
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    try:
        udpSocket.bind((UDPip,UDPport))
    except OSError as e:
        log(e)
    udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    udpSocket.settimeout(timeout)
    udpSocket.setsockopt(SOL_SOCKET, SO_RCVBUF, 1024)
    recivedMessage, address = udpSocket.recvfrom(1024)
    udpSocket.close()
    return recivedMessage, address[0]

def BroadcastMessage(message, port):
    log("Message: %s on port %s"%(message, str(port)))
    udpSocket = PrepareUDPSocket(port)
    udpSocket.sendto(message.encode(),('<broadcast>',int(port)))
    udpSocket.close()
    
def PrepareUDPSocket(port):
    UDPip = getLocalIP()
    UDPport = int(port)
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    try:
        udpSocket.bind((UDPip,UDPport))
    except OSError as e:
        log("prepareUDPSocket error: %s with port %s" %(e,port))
        udpSocket.close()
    udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    udpSocket.setsockopt(SOL_SOCKET, SO_RCVBUF, 1024)
    udpSocket.settimeout(0.3)
    return udpSocket


def CatchMessage(port):
    searchTime = 3;
    startTime = time.time()
    msg = ""
    ipAddress = ""
    while (time.time() - startTime) < searchTime:
        UDPip = getLocalIP()
        UDPport = port
        udpSocket1 = PrepareUDPSocket(UDPport)
        try:
            msg, (ipAddress,_) = udpSocket1.recvfrom(1024)
            log(msg)
            udpSocket1.close()
        except:
            msg = ""
            ipAdress = ""
            udpSocket1.close()
            continue
        return msg, ipAddress
    
