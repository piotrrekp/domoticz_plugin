import os
import unittest
import string
CFGFILE = "allmodule.cfg"
MACFILE  = "macList"
EXTENSION = ".cfg"

class config(object):
    def __init__(self, path, hardwareid):
        self.mac = ""
        self.ip = ""
        self.plugintype = ""
        self.moduletype = ""
        self.hardwareid = hardwareid
        self.configfile = self.set_cfgfile_path(path)
        self.maclistfile = self.set_cfgfile_path(path, MACFILE)
        if self.exist():
            self.read()
        
    def set_cfgfile_path(self, path, file = ""):
        if not file: file = str(self.hardwareid)
        cfgfile = ""
        if path[-1] == "/":
            cfgfile = path + file + EXTENSION 
        else: 
            cfgfile = path + "/" + file + EXTENSION  
        return cfgfile
    
    def set_config(self, newmodule):
        hid, mac, ip, plugintype, moduletype = newmodule
        self.hardwareid = hid
        self.set_mac(mac)
        self.set_ip(ip)
        self.set_plugin_type(plugintype)
        self.set_module_type(moduletype.strip(string.whitespace))
    
    def check_mac(self, mac):
        maclist = []
        if self.exist(self.maclistfile):
            with open(self.maclistfile, 'r') as macfile:
                for line in macfile:
                    maclist.append(line.split(' '))
        else:
            with open(self.maclistfile, 'w'):
                pass
        return True if mac in maclist else False
        
    def set_mac(self, mac):
        self.mac = mac

    def set_ip(self,ip):
        self.ip = ip

    def set_plugin_type(self, pluginType):
        self.plugintype = pluginType
    
    def set_module_type(self, moduleType):
        self.moduletype = moduleType
        
    def exist(self, file = -1):
        if file == -1: 
            file =  self.configfile
        return os.path.isfile(file)
    
    def read(self):
        with open(self.configfile, "r") as cfg:
            self.mac,self.ip,self.moduletype, self.plugintype = cfg.readline().split(",")
    
    def get_module_type(self): 
        return self.moduletype
        
    def get_type(self):
        return self.plugintype
    
    def get_mac(self):
        return self.mac
    
    def get_ip(self):
        return self.ip
    def get_config(self):
        return (self.hardwareid, self.mac, self.ip, self.plugintype, self.moduletype)
        
    def remove(self):
        if self.exist():
            os.remove(self.configfile)
    
    def write(self):
        data = ",".join([self.mac,self.ip,self.moduletype, self.plugintype])
        print(self.configfile, data)
        with open(self.configfile, "w") as cfg:
            cfg.write(data)




class TotalConfig(object):
    def __init__(self, path):
        """
        cfgfile structure:
        hardwareid mac ip moduletype plugintype
        """
        self.allconfig = []
        self.cfgfile = self.set_cfgfile_path(path)
        self.read()
    
    def set_cfgfile_path(self, path):
        cfgfile = ""
        if path[-1] == "/":
            cfgfile = path + CFGFILE
        else: 
            cfgfile = path + "/" + CFGFILE
        return cfgfile
    
    def read(self):
        if self.exist():
            self.allconfig = []
            with open(self.cfgfile, 'r') as cfg:
                for line in cfg:
                    if line != "": self.allconfig.append(line.split(' '))
    
    def write(self, newmodule):
        hid, mac, _, _, _ = newmodule
        if self.hardwareid_is_stored(hid) or self.mac_is_stored(mac): 
            return
        else:
            data = " ".join(newmodule) + "\n"
            
            if self.exist():
                with open(self.cfgfile, 'a') as cfg:
                    cfg.write(data)
            else:
                with open(self.cfgfile, 'w') as cfg:
                    cfg.write(data)
    
    def exist(self):
        return os.path.isfile(self.cfgfile)
    
    def print_all(self):
        print(self.allconfig)
        print(len(self.allconfig))
        for module in self.allconfig:
            print(" ".join(module))
    
            
    def mac_is_stored(self, mac):
        self.read()
        for module in self.allconfig:
            _, storedmac, _, _, _ = module
            if mac == storedmac:
                return True
        else:
            return False
        
    def hardwareid_is_stored(self,hid):
        hid = str(hid)
        self.read()
        print(self.allconfig)
        for module in self.allconfig:
            storedhid, _, _, _, _ = module
            if hid == storedhid:
                return True
        else:
            return False
        
    def get_line_with_mac(self, mac):
        self.read()
        if self.mac_is_stored(mac):
            for module in self.allconfig:
                _, storedmac, _, _, _ = module
                if mac == storedmac:
                    return module
            else:
                raise ValueError
    
    def get_line_with_hid(self, hid):
        self.read()
        if self.hardwareid_is_stored(hid):
            for module in self.allconfig:
                storedhid, _ , _, _, _ = module
                if str(hid)== storedhid:
                    return module
            else:
                return None
            
#     def update_module(self, hardwareid, newmodule):
#         self.read()
#         if self.hardwareid_is_stored(hardwareid):
#             for module in self.allconfig:
#                 hid, _,_,_,_ = module
#                 
#                 if hid == str(hardwareid):
#                     self.allconfig.remove(module)
#                     self.allconfig.append(newmodule)
#                     break
#             self.allconfig.sort()
#             self.write_all()
    
    def remove_module(self,hardwareid):
        self.read()
        module = self.get_line_with_hid(hardwareid)
        self.allconfig.remove(module)
        self.write_all()
        
    def update_module(self, hardwareid, newmodule):
        self.read()
        module = self.get_line_with_hid(hardwareid)
        self.allconfig.remove(module)
        hid,mac,ip,mt,pt = newmodule
        data = [str(hid), mac, ip, mt, pt]
        self.allconfig.append(data)
        self.write_all()

    def write_all(self):
        os.remove(self.cfgfile)
        with open(self.cfgfile, 'w') as cfg:
            for module in self.allconfig:
                print(module)
                data = " ".join(module)
                cfg.write(data)
            
              
     
class TestConfigClass(unittest.TestCase):
    
    def setUp(self):
        self.cfg = config("/home/piotrrek/config", 2)
        self.cfg.set_mac("AA:BB:CC:DD:EE:FF")
          
    def test_prepare_filename(self):
        expected = self.cfg.configfile
        result = "/home/piotrrek/config/2.cfg"
        self.assertEqual(result, expected)
        cfg1 = config("/home/piotrrek/config/", 2)
        result = cfg1.configfile
        expected = "/home/piotrrek/config/2.cfg"
        self.assertEqual(result, expected)
    
    def test_create_ports(self):
        self.assertEqual(self.cfg.sendingport, 60004)
        self.assertEqual(self.cfg.recivingport, 60005)
        conf = config("bla/bla/bla",3)
        self.assertEqual(conf.sendingport, 60006)
        self.assertEqual(conf.recivingport, 60007)
        conf = config("bla/bla/bla",4)
        self.assertEqual(conf.sendingport, 60008)
        self.assertEqual(conf.recivingport, 60009)
    
    def test_is_new_cfg(self):
        if os.path.isfile("/home/piotrrek/config/4.cfg"):
            os.remove("/home/piotrrek/config/4.cfg")
        cfg = config("/home/piotrrek/config", 4)
        self.assertEqual(cfg.exist(), False)
        with open("/home/piotrrek/config/4.cfg", "w"):  pass
        self.assertEqual(cfg.exist(),True)
        
    def test_write_and_read(self):
        cfg = config("/home/piotrrek/config",2)
        cfg.set_mac("AA:BB:CC:DD:EE:FF")
        cfg.set_plugin_type("M1W")
        cfg.set_module_type("THP")
        cfg.write()
        
        cfg1 = config("/home/piotrrek/config",2)
        cfg1.read()
        self.assertEqual(cfg1.moduletype, "THP")
        self.assertEqual(cfg1.plugintype, "M1W")
        self.assertEqual(cfg1.mac, "AA:BB:CC:DD:EE:FF")
    
    def test_write_and_write(self):
        cfg = config("/home/piotrrek/config",3)
        cfg.set_mac("AA:BB:CC:DD:EE:FF")
        cfg.set_module_type("THP")
        cfg.set_plugin_type("THP")
        cfg.write()
        cfg = config("/home/piotrrek/config",3)
        cfg.set_mac("AA:BB:CC:DD:EE:FF")
        cfg.set_module_type("M1W")
        cfg.set_plugin_type("M1W")
        cfg.write()
        self.assertEqual(cfg.mac, "AA:BB:CC:DD:EE:FF")
        self.assertEqual(cfg.moduletype, "M1W")
        
    def test_read_edit_and_write(self):
        cfg = config("/home/piotrrek/config",3)
        cfg.set_module_type("THP")
        cfg.write()
        cfg1 = config("/home/piotrrek/config",3)
        cfg1.read()
        cfg1.write()
        self.assertEqual(cfg1.moduletype, "THP")
    def test_mac_in_commonlist(self):
        result = self.cfg.check_mac("AA:BB:CC:DD:EE:FF")
        expected = False
        self.assertEqual(result, expected)
        
    def test_list_of_tuple_edit(self):
        lista = [(1,'a'),(2,'b'),(3,'c')]
        numer = 2
        nowakrotka = (2,'d')
        for module in lista:
            n,c = module
            if n == numer:
                lista.remove(module)
                lista.append(nowakrotka)
        nowalista = [(1,'a'),(2,'d'),(3,'c')]
        lista.sort()
        self.assertEqual(lista, nowalista)
        

        
if __name__ == '__main__':
    
#     unittest.main()
   
    
    if not os.path.isdir("/home/piotrrek/config/mic2/config"):
        os.makedirs("/home/piotrrek/config/mic2/config")
    os.chdir("/home/piotrrek/config/mic2/config")
    print(os.getcwd())
    bloker1 = locky("1")
    bloker1.lock()
    
    bloker2 = locky("2")
    print(bloker1.anyLockFileExist())
    bloker2.lock()
