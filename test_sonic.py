# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from bs4 import BeautifulSoup
import os
import hashlib
import re
from html2text import html2text
import thread
import threading
import SendKeys
import win32con
import win32gui
from bs4 import BeautifulSoup
import configparser


class login(object):
    Address_Objects = (By.LINK_TEXT,"Address Objects")


    def __init__(self):
        self.driver = webdriver.Firefox()


    def login_web(self, base_url):
#        base_url = self.base_url = "https://10.8.42.58/"
        driver = self.driver
        driver.implicitly_wait(30)
#        driver.maximize_window()
#        base_url = "http://10.8.42.2/"
        driver.get(base_url + "auth.html")
#    driver.switch_to.window("SonicWall Administrator")
        driver.switch_to.frame("authFrm")
        driver.find_element_by_name("userName").clear()
        driver.find_element_by_name("userName").send_keys("admin")
        driver.find_element_by_name("pwd").clear()
        driver.find_element_by_name("pwd").send_keys("password")
        driver.find_element_by_name("Submit").click()

    def logout(self):
        self.driver.quit()

    def switch_to_object(self):
        driver = self.driver
        driver.switch_to.default_content()
        driver.switch_to.frame('logoFrame')
        driver.find_element_by_xpath(".//*[@id='nav_manage']").click()
        driver.switch_to.default_content()
        driver.switch_to.frame("outlookFrame")
        driver.find_element_by_link_text("Objects").click()
#        address_objects = self.driver.find_element('Network')
#        driver.execute_script("arguments[0].click();", address_objects)
        time.sleep(2)

    def switch_to_rules(self):
        driver = self.driver
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame('logoFrame')
        driver.find_element_by_xpath(".//*[@id='nav_manage']").click()
        driver.switch_to.default_content()
        driver.switch_to.frame("outlookFrame")
        driver.find_element_by_link_text("Rules").click()
#        address_objects = self.driver.find_element('Network')
#        driver.execute_script("arguments[0].click();", address_objects)
        time.sleep(2)

    def switch_to_interface(self):
        driver = self.driver
        driver.switch_to.default_content()

        driver.switch_to.frame('logoFrame')
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='nav_manage']").click()
        driver.switch_to.default_content()
        driver.switch_to.frame('outlookFrame')
        button = driver.find_element_by_link_text('Network')
        driver.execute_script('arguments[0].click()', button)
        time.sleep(2)

    def switch_to_default_window(self):
        driver = self.driver
        all_handles = driver.window_handles
        current_handle = driver.current_window_handle
        for handle in all_handles:
            if handle != current_handle:
                driver.switch_to.window(handle)

    def switch_window(self, windowname):
        driver = self.driver
        driver.maximize_window()
        driver.switch_to.default_content()
        all_handles = driver.window_handles
        for handle in all_handles:
            driver.switch_to.window(handle)
            if driver.title == windowname:
                driver.switch_to.window(handle)
                break
        print driver.title

    def test_get_conf_info(self):
        cp1 = configparser.ConfigParser()
        cp1.read('DSLite.cfg')
        return cp1

    def test_configure_interface(self, location):
        driver= self.driver
        driver.switch_to.default_content()
        cp = self.test_get_conf_info()
        self.switch_to_interface()
        driver.switch_to.default_content()
        driver.switch_to.frame("tabFrame")
        if location == 'local':
         #   driver.switch_to.default_content()
            driver.find_element_by_id("ifaceType4").click()
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='0']/td[11]/a/img").click()
            self.switch_window("Edit Interface - X0")
            driver.find_element_by_name("lan_iface_lan_ip").clear()
            driver.find_element_by_name("lan_iface_lan_ip").send_keys("%s" %cp.get("local_ds_lite", 'local_x0_ip'))
            driver.find_element_by_css_selector("input.snwl-btn.snwl-btn-primary").click()
            time.sleep(2)
            self.switch_to_default_window()
            driver.switch_to.default_content()
            driver.switch_to.frame("tabFrame")
            driver.find_element_by_id("ifaceType6").click()
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='1']/td[9]/a/img").click()
            self.switch_window('Edit Interface - X1 for IPv6')
            Select(driver.find_element_by_name("ipv6_iface_mode")).select_by_visible_text("Static")
            driver.find_element_by_name("ipv6_iface_static6_ip").clear()
            driver.find_element_by_name("ipv6_iface_static6_ip").send_keys("%s" %cp.get("local_ds_lite", 'local_ipv6'))
            driver.find_element_by_name("ipv6_iface_static6_gateway").clear()
            driver.find_element_by_name("ipv6_iface_static6_gateway").send_keys("%s" %cp.get("local_ds_lite", 'local_ipv6_gateway'))
            driver.find_element_by_css_selector("input.snwl-btn.snwl-btn-primary").click()
            print driver.current_url
            self.switch_to_default_window()
            print driver.current_url
        elif location == 'remote':
            driver.find_element_by_id("ifaceType4").click()
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='0']/td[11]/a/img").click()
            self.switch_window("Edit Interface - X0")
            driver.find_element_by_name("lan_iface_lan_ip").clear()
            driver.find_element_by_name("lan_iface_lan_ip").send_keys("%s" %cp.get("remote_ds_lite", 'local_x0_ip'))
            driver.find_element_by_css_selector("input.snwl-btn.snwl-btn-primary").click()
            time.sleep(2)
            self.switch_to_default_window()
            driver.switch_to.default_content()
            driver.switch_to.frame("tabFrame")
            driver.find_element_by_id("ifaceType6").click()
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='1']/td[9]/a/img").click()
            self.switch_window('Edit Interface - X1 for IPv6')
            Select(driver.find_element_by_name("ipv6_iface_mode")).select_by_visible_text("Static")
            driver.find_element_by_name("ipv6_iface_static6_ip").clear()
            driver.find_element_by_name("ipv6_iface_static6_ip").send_keys("%s" %cp.get("remote_ds_lite", 'local_ipv6'))
            driver.find_element_by_name("ipv6_iface_static6_gateway").clear()
            driver.find_element_by_name("ipv6_iface_static6_gateway").send_keys("%s" %cp.get("remote_ds_lite", 'local_ipv6_gateway'))
            driver.find_element_by_css_selector("input.snwl-btn.snwl-btn-primary").click()
            self.switch_to_default_window()

    def test_add_DSLite(self, location):
        driver= self.driver
        time.sleep(2)
        cp = self.test_get_conf_info()
#        self.switch_to_interface()
        driver.switch_to.default_content()
        time.sleep(2)
        driver.switch_to.frame("tabFrame")
        driver.find_element_by_id("ifaceType4").click()
        time.sleep(2)
        Select(driver.find_element_by_id("addIfaceSelectCtrl")).select_by_visible_text("4to6 Tunnel Interface")
        self.switch_window('Add DS-Lite Softwire Interface')
        if location == 'local':
            driver.find_element_by_name("tunnel_iface_name").clear()
            driver.find_element_by_name("tunnel_iface_name").send_keys("%s" %cp.get("local_ds_lite", 'ds_lite_name'))
            driver.find_element_by_id("tunnel_iface_softwire_loc_v6ip").clear()
            driver.find_element_by_id("tunnel_iface_softwire_loc_v6ip").send_keys("%s" %cp.get("local_ds_lite", 'local_ipv6'))
            driver.find_element_by_id("tunnel_iface_softwire_remote_v6ip").clear()
            driver.find_element_by_id("tunnel_iface_softwire_remote_v6ip").send_keys("%s" %cp.get("local_ds_lite", 'remote_ipv6'))
            driver.find_element_by_link_text("Advanced").click()
            driver.find_element_by_id("tunnel_iface_softwire_loc_v4ip").clear()
            driver.find_element_by_id("tunnel_iface_softwire_loc_v4ip").send_keys("%s" %cp.get("local_ds_lite", 'local_ipv4'))
            driver.find_element_by_css_selector("input.snwl-btn.snwl-btn-primary").click()
            self.switch_to_default_window()
        elif location == 'remote':
            driver.find_element_by_name("tunnel_iface_name").clear()
            driver.find_element_by_name("tunnel_iface_name").send_keys("%s" %cp.get("remote_ds_lite", 'ds_lite_name'))
            driver.find_element_by_id("tunnel_iface_softwire_loc_v6ip").clear()
            driver.find_element_by_id("tunnel_iface_softwire_loc_v6ip").send_keys("%s" %cp.get("remote_ds_lite", 'local_ipv6'))
            driver.find_element_by_id("tunnel_iface_softwire_remote_v6ip").clear()
            driver.find_element_by_id("tunnel_iface_softwire_remote_v6ip").send_keys("%s" %cp.get("remote_ds_lite", 'remote_ipv6'))
            driver.find_element_by_link_text("Advanced").click()
            driver.find_element_by_id("tunnel_iface_softwire_loc_v4ip").clear()
            driver.find_element_by_id("tunnel_iface_softwire_loc_v4ip").send_keys("%s" %cp.get("remote_ds_lite", 'local_ipv4'))
            driver.find_element_by_css_selector("input.snwl-btn.snwl-btn-primary").click()
            time.sleep(2)
            self.switch_to_default_window()

    def test_add_ao(self, location):
        driver = self.driver
        cp = self.test_get_conf_info()
        driver.switch_to.default_content()
        self.switch_to_object()
        driver.find_element_by_link_text("Address Objects").click()
        time.sleep(2)
        driver.switch_to.default_content()
        driver.switch_to.frame("tabFrame")
        time.sleep(2)
        button = driver.find_element_by_xpath(".//*[@id='commonAddBtn']")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        self.switch_window("Add Address Object")
        if location == 'local':
            driver.find_element_by_name('noName').clear()
            driver.find_element_by_name('noName').send_keys("%s" %cp.get("local_ds_lite", 'remote_x0_subnet'))
            Select(driver.find_element_by_name("zone")).select_by_visible_text("LAN")
            Select(driver.find_element_by_name("noType")).select_by_visible_text("Network")
            driver.find_element_by_id("noIp1").clear()
            driver.find_element_by_id("noIp1").send_keys("%s" %cp.get("local_ds_lite", 'remote_x0_subnet'))
            driver.find_element_by_id("noIp2").clear()
            driver.find_element_by_id("noIp2").send_keys("255.255.255.0")
            button = driver.find_element_by_id("actionBtn0")
            driver.execute_script("arguments[0].click();", button)
            self.switch_to_default_window()
        elif location == 'remote':
            driver.find_element_by_name('noName').clear()
            driver.find_element_by_name('noName').send_keys("%s" %cp.get("remote_ds_lite", 'remote_x0_subnet'))
            Select(driver.find_element_by_name("zone")).select_by_visible_text("LAN")
            Select(driver.find_element_by_name("noType")).select_by_visible_text("Network")
            driver.find_element_by_id("noIp1").clear()
            driver.find_element_by_id("noIp1").send_keys("%s" %cp.get("remote_ds_lite", 'remote_x0_subnet'))
            driver.find_element_by_id("noIp2").clear()
            driver.find_element_by_id("noIp2").send_keys("255.255.255.0")
            button = driver.find_element_by_id("actionBtn0")
            driver.execute_script("arguments[0].click();", button)
            self.switch_to_default_window()

    def test_add_ds_lite_route(self, location):

        driver = self.driver
        time.sleep(2)
        cp = self.test_get_conf_info()
        self.switch_to_interface()
        driver.find_element_by_link_text('Routing').click()
        time.sleep(1)
        driver.switch_to.default_content()
        driver.switch_to.frame("tabFrame")
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='pbrFolder_trigger']").click()
        time.sleep(1)
        driver.find_element_by_id('commonAddBtn').click()
        time.sleep(2)
        self.switch_window('Add Route Policy')
        if location == 'local':
            Select(driver.find_element_by_id('source')).select_by_visible_text('Any')
            Select(driver.find_element_by_id('destination')).select_by_visible_text("%s" %cp.get("local_ds_lite", 'remote_x0_subnet'))
            Select(driver.find_element_by_id('service')).select_by_visible_text('Any')
            Select(driver.find_element_by_id('iface')).select_by_visible_text("%s" %cp.get("local_ds_lite", 'ds_lite_name'))
            time.sleep(2)
        #    Select(driver.find_element_by_id('iface')).select_by_visible_text("%s" %cp.get("local_ds_lite", 'ds_lite_name'))
            driver.find_element_by_name('metric').clear()
            print 'tessss'
            driver.find_element_by_name('metric').send_keys('10')
            time.sleep(1)
            driver.find_element_by_name('ok').click()
            self.switch_to_default_window()

        elif location == 'remote':
            Select(driver.find_element_by_id('source')).select_by_visible_text('Any')
            Select(driver.find_element_by_id('destination')).select_by_visible_text("%s" %cp.get("remote_ds_lite", 'remote_x0_subnet'))
            Select(driver.find_element_by_id('service')).select_by_visible_text('Any')
            Select(driver.find_element_by_id('iface')).select_by_visible_text("%s" %cp.get("remote_ds_lite", 'ds_lite_name'))
            time.sleep(1)
            driver.find_element_by_name('metric').clear()
            driver.find_element_by_name('metric').send_keys('10')
            driver.find_element_by_name('ok').click()
            self.switch_to_default_window()

    def test_enable_rule(self):
        driver = self.driver
        self.switch_to_rules()
        driver.find_element_by_link_text('Access Rules').click()
        time.sleep(1)
        driver.switch_to.default_content()
        driver.switch_to.frame("tabFrame")
        time.sleep(2)
        driver.find_element_by_css_selector("#ruleFromZoneSelect > span.actionValue").click()
        driver.find_element_by_xpath("//*[@id='ruleFromZoneSelect']/ul/li[3]/span").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#ruleToZoneSelect > span.actionValue").click()
        driver.find_element_by_xpath("//*[@id='ruleToZoneSelect']/ul/li[2]/span").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#commonFolderIPVersionSel > span.actionValue").click()
        driver.find_element_by_xpath(".//*[@id='commonFolderIPVersionSel']/ul/li[1]").click()

        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='0']/td[21]/img[2]").click()
        time.sleep(1)
        self.switch_window('Edit Rule')
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='p1panel0']/table[2]/tbody/tr[1]/td[2]/input[1]").click()
        driver.find_element_by_name("ok").click()
        self.switch_to_default_window()

















test = login()
test.login_web('https://10.8.42.58/')
test.test_enable_rule()
'''
#test.test_enable_firewall_settings()
test.test_configure_interface('local')
test.test_add_DSLite('local')

#test.test_upload_firmware()
#test.switch_to_default_window()
test.test_add_ao('local')
test.test_add_ds_lite_route('local')
#test.test_upload_firmware()

test.test_enable_firewall_settings()
if test.test_boot_new_firmware() == False:
    test.test_upload_firmware()
    test.test_boot_new_firmware()
else:
    test.test_boot_new_firmware()
'''
#test.test_enable_firewall_settings()
#test.logout()