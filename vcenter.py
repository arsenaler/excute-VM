#!/usr/sbin/python
# -*- coding: utf-8 -*-

import os
import os.path
import time
from pysphere import VIServer
from pysphere import VIException, VIApiException, FaultTypes
import logging
from pysphere.resources import VimService_services as VI

import subprocess


class vcenter(object):
    '''
    ip = ''
    user = ''
    pwd = ''
    connect_flag = False
    server = None
    '''
    @classmethod
    def connect_server(cls,ip, user, pwd):
        cls.ip = ip
        cls.user = user
        cls.pwd = pwd
        cls.server = VIServer()
        cls.server.connect(cls.ip, cls.user, cls.pwd)
        print "if you use the vm.login_in_guest(), you must install vmware tools in the vm"
        cls.connect_flag = cls.server.is_connected()
        if cls.connect_flag:
            return True
        return False


    @classmethod
    def get_vm(cls, name):
        vm = cls.server.get_vm_by_name(name)
 #       subprocess.call(['ifconfig', 'eth0', 'up'])
        return vm

    @classmethod
    def get_hosts_by_name(cls, from_mor):
        try:
            hosts = cls.server.get_hosts(from_mor)
            return hosts
        except:
            print "the server doesn't connect"
            return None

    @classmethod
    def get_all_hosts(cls):
        return cls.server.get_hosts()

    @classmethod
    def disconnnect_server(cls):
        if cls.connect_flag == True:
            cls.disconnect = cls.server.disconnect()
            cls.connect_flag = False

    @classmethod
    def power_on_vm(cls, name):
        try:
            vm = cls.server.get_vm_by_name(name)
            if (vm.is_powered_off()):
                vm.power_on()
                print 'the vm is off, we will power on it'
                print 'now we power on the PC--' + name
                print 'we will wait for 100 seconds'
                time.sleep(100)
            else:
                print 'the PC -- ' + name + ' is already power on'
        except:
            print "pc is error"

    @classmethod
    def power_off_vm(cls, name):
        try:
            vm = cls.server.get_vm_by_name(name)
            if (vm.is_powered_on()):
                vm.power_off()
                print "now we power off the " + name
            else:
                print 'now the ' + name + ' is power off'
        except:
            print 'the '+ name + "  is error"

    @classmethod
    def get_all_vms(cls):
        return cls.server.get_registered_vms()

    @classmethod
    def login_vm(cls,name, user, pwd):
        vm = cls.server.get_vm_by_name(name)
        vm.login_in_guest(user, pwd)
        subprocess.call(['ifconfig', 'eth0 down'])
        vm.make_directory(r"c:\my\binary")

    @classmethod
    def create_snapshot(cls,vm_name,snap_name):
        vm = cls.server.get_vm_by_name(vm_name)
        return vm.create_snapshot(snap_name)

    @classmethod
    def delete_snapshot(cls, vm_name, snap_name):
        vm = cls.server.get_vm_by_name(vm_name)
        vm.delete_named_snapshot(snap_name)

    @classmethod
    def get_snaplist(cls, vm_name):
        vm = cls.server.get_vm_by_name(vm_name)
        return vm.get_snapshots()

    @classmethod
    def vm_clone(cls, vm_name,new_vm):
        vm = cls.server.get_vm_by_name(vm_name)
        vm.clone(new_vm)
    '''
    @classmethod
    def ChangeVM_IP(cls, vm_name,vm_user, vm_os,vm_ip,vm_netmask,vm_gateway,vm_main_dns,vm_passwd=None):
        vm = cls.server.get_vm_by_name(vm_name)
        vm.login_in_guest(vm_user, vm_passwd)
        print vm.get_status()
        if vm_os=='ubuntu':
            cmd_path='/bin/echo'
            #echo ces | sudo -S /opt/ecloud/reconfig_ubuntu_network.sh'
            cmd_args = [vm_passwd, '|', 'sudo', '- S', '/home/qa/interface.sh', vm_ip, vm_netmask, vm_gateway, vm_main_dns]
            try:
                pid = vm.start_process(cmd_path, args=cmd_args)
                print pid
                time.sleep(20)
                return True
            except Exception, e:
                msg='Error in executing change ip command for %s.' % vm.get_property('name')
                logging.error(msg)
                return False
    '''
    # if you use the vm.login_in_guest, you must install vmware-tools in the vm
    @classmethod
    def get_vm_ip(cls, vm_name, vm_user, vm_passwd, vm_vlan, iptype):

        vm = cls.server.get_vm_by_name(vm_name)
        vm.login_in_guest(vm_user, vm_passwd)
        net = vm.get_property('net',from_cache=False)
        for i in range(0, len(net)):
            ip_address = net[i].get('ip_addresses')
            ip_network = net[i].get('network')
            if ip_network == vm_vlan:
                if iptype == 'ipv4':
                    return ip_address[0]
                elif iptype == 'ipv6':
                    return ip_address[1]

    @classmethod
    def get_vm_eth0_ip(cls,vm_name, vm_user, vm_passwd):
        vm = cls.server.get_vm_by_name(vm_name)
        vm.login_in_guest(vm_user, vm_passwd)
        return vm.get_property('ip_address', from_cache=False)
'''
server = vcenter()
server.connect_server("10.8.2.21", 'root', 'sonicpassword')


ip1111=server.get_vm_ip('wdong-veth0', 'qa', 'password','sonicos-167', 'ipv6')
print ip1111
print '===============+++++++++++++'
print server.get_vm_eth0_ip('wdong-ubuntu14-2', 'wdong', 'password')


vm1 = server.get_vm('ubuntu server 16.04-sonicos-4core')
vm1.login_in_guest('wdong', 'password')
ip = vm1.get_properties()
for key,value in ip.items():

    print key, value

#print vm.get_status()
#server.create_snapshot('wdong-XP72','test1')
#server.delete_snapshot('wdong-XP12','test')
#server.vm_clone('wdong-XP12','wdong-test')

vms = server.get_all_vms()
for vm in vms:
    if 'wdong' in vm:
        print vm
#print server.get_all_hosts()


vm = server.get_vm('wdong-veth0')
vm.login_in_guest('qa', 'password')
lst = vm.list_processes()
print '==========================='
print vm.get_property('ip_address', from_cache=False)
net = vm.get_property('net',from_cache=False)
print net
#dict = {}
lst11 = lst12 =[]
for i in range(0, len(net)):
#    print net[i].get('ip_addresses'), net[i].get('network')
    ip_address = net[i].get('ip_addresses')
    ip_network = net[i].get('network')
    if ip_network != None:
        print ip_address
    lst11.append(ip_address)
    lst12.append(ip_network)
#dict = { key:value for key in lst11 and value in lst12 }
#print dict
#vm.make_directory('/home/qa/testing1', create_parents=True)

print '==============================='
dict =  vm.get_properties(from_cache=False)
for key, value in dict.iteritems():
    print key, value
#cmd_path='/sbin/ifconfig'
#cmd_args = [vm_passwd, '|', 'sudo'
#vm.start_process('/sbin', 'ifconfig', 'eth0', 'down')
'''
'''
def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret
#    print lst


#pid = server.ChangeVM_IP('wdong-Swat', 'qa', 'ubuntu', '9.9.9.9', '255.255.240.0', '9.9.9.1',  '10.190.202.200', 'password')
#print pid


#pid1 = vm.start_process('cmd.exe', args=["/c netsh interface ip set address \"Local Area Connection 4\" static 192.168.0.10 255.255.255.0 192.168.0.1 1"])


#for cmd in lst:
#    print cmd
#vm.create_snapshot('mysnap')
server.disconnnect_server()


'''