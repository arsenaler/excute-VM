from vcenter import *
from ssh import *
from latest_build1 import *
import time
import testtest
import os, re, urllib
import paramiko
import configparser
import threading
import autopep8


def test_configure_local_dslite(base_url, local):
    login = testtest.login()
    login .login_web(base_url)
    login.test_configure_interface('local')
    login.test_add_DSLite('local')
    login.test_add_ao('local')
    login.test_add_ds_lite_route('local')
    login.test_enable_rule()
    time.sleep(2)
    login.logout()

def test_configure_remote_dslite(base_url, remote):
    login = testtest.login()
    login .login_web(base_url)
    login.test_configure_interface('remote')
    time.sleep(1)
    login.test_add_DSLite('remote')
    login.test_add_ao('remote')
    login.test_add_ds_lite_route('remote')
    login.test_enable_rule()
    time.sleep(2)
    login.logout()


def test_get_conf_info():
    cp = configparser.ConfigParser()
    cp.read('DSLite.cfg')
    return cp





def test_connect_vm_server():
    cp = test_get_conf_info()
    server = cp.items('vm_server')
    vcenter.connect_server(server[0][1],server[1][1], server[2][1])
'''
def test_get_vm_ip(vm_name):
    test_connect_vm_server()
    vm_info = test_get_vm(vm_name)
    vcenter.power_on_vm(vm_info[0][1])
    return vcenter.get_vm_eth0_ip(vm_info[0][1], vm_info[1][1], vm_info[2][1])


def test_cmd_on_vm(vm_name, command):
    vm_info = test_get_vm(vm_name)
    vm_ip = test_get_vm_ip(vm_name)
    test_ssh.test_connect(vm_ip, 22, vm_info[1][1], vm_info[2][1])
    return test_ssh.test_cmd(command)
'''
def test_get_vm_ip(location, vlan, version):
    cp = test_get_conf_info()
    test_connect_vm_server()
    if location == 'local':
        vm_info = cp.items('local_vm')
        vcenter.power_on_vm(vm_info[0][1])
        vm_ip = vcenter.get_vm_ip(vm_info[0][1], vm_info[1][1], vm_info[2][1], vlan, version)
        print vm_ip
        return vm_ip
    elif location == 'remote':
        vm_info = cp.items('remote_vm')
        vcenter.power_on_vm(vm_info[0][1])
        vm_ip = vcenter.get_vm_ip(vm_info[0][1], vm_info[1][1], vm_info[2][1], vlan, version)
        print vm_ip
        return vm_ip





def test_local_vm(location, command):
    cp = test_get_conf_info()
    server = cp.items('vm_server')
    vcenter.connect_server(server[0][1], server[1][1], server[2][1])
    print 'test'
    if location == 'local':
        vm_info = cp.items('local_vm')
        vcenter.power_on_vm(vm_info[0][1])
        vm_ip = vcenter.get_vm_eth0_ip(vm_info[0][1], vm_info[1][1], vm_info[2][1])
        test_ssh.test_connect(vm_ip, 22, vm_info[1][1], vm_info[2][1])
        t = test_ssh.test_cmd(command)
        print t
    elif location == 'remote':
        vm_info = cp.items('remote_vm')
        vcenter.power_on_vm(vm_info[0][1])
        vm_ip = vcenter.get_vm_eth0_ip(vm_info[0][1], vm_info[1][1], vm_info[2][1])
        test_ssh.test_connect(vm_ip, 22, vm_info[1][1], vm_info[2][1])
        t = test_ssh.test_cmd(command)
        print t





test_configure_local_dslite('https://10.8.42.58/', 'local')
test_configure_remote_dslite('https://10.8.43.60/', 'remote')

#test_local_vm('local', 'ping %s >ping.txt'%test_get_vm_ip('remote', 'wdong_vlan558', 'ipv4'))
#test_local_vm('remote', 'ping %s'%test_get_vm_ip('local', 'wdong_vlan421', 'ipv4'))

'''
if __name__ == "__main()__":
    threads = []
    t1 = threading.Thread(test_configure_local_dslite('https://10.8.42.58/', 'local', 'wdong-ubuntu14-2', 'll'))
    threads.append(t1)
    t2 = threading.Thread(test_configure_remote_dslite('https://10.8.43.60/', 'remote', 'wdong-ubuntu14-3', 'll'))
    threads.append(t2)
    t3 = threading.Thread(test_local_vm('local', 'ping %s'%test_get_vm_ip('remote', 'wdong_vlan558', 'ipv4')))
    threads.append(t3)
    t4 = threading.Thread(test_local_vm('remote', 'ping %s'%test_get_vm_ip('local', 'wdong_vlan421', 'ipv4')))
    threads.append(t4)
    for t in threads:
        t.start()
    for t in threads:
#        t.join()
'''