import os
import os.path
import time
import socket
import sys
import string
import ssl
import base64
from pysphere import VIServer
from pysphere import VIException, VIApiException, FaultTypes


class control:
    
    ip = ''    
    user = ''
    pwd = ''
    connect_flag = False
    server = None
    
    def connect_server(self,ip, user,pwd):
        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.server = VIServer()
        self.server.connect(self.ip, self.user, self.pwd)
        self.connect_flag = self.server.is_connected()  
        if self.connect_flag:  
            return True  
        return False          
    
    
    def get_vm(self, name):
        vm = self.server.get_vm_by_name(name)
        print vm.get_status()
        return vm
    
    
    def disconnnect_server(self):
        if self.connect_flag == Ture:
            self.disconnect = self.server.disconnect()
            self.connect_flag = False
        
        
        
control1 = control()

control1.connect_server("10.8.2.21", 'root', 'sonicpassword')
control1.get_vm('wdong-XP72')
        
        