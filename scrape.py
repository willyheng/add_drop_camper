#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 10:10:12 2019

@author: willy
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import re
from time import gmtime, strftime, sleep
import yaml
import logging

def site_login():
    driver.find_element_by_id("username").send_keys(USERNAME)
    driver.find_element_by_id ("password").send_keys(PASSWORD)
    driver.find_element_by_name("submitLogin").click()
    driver.refresh()
    
def site_refresh():
    driver.refresh()
    # Wait until loaded
    element = WebDriverWait(driver, 1).until(lambda x:    x.find_element_by_class_name('sectionsViewSectionsTable_32_3'))


def found_course(driver, course_code, stream_id):
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    for s in stream_id:
        search_results = page_soup.find_all(text = re.compile('.*'+course_code+'.*'))[s].parent.parent.parent.find('a', attrs={'class':'actionItem'}, text = 'change stream')
        if search_results != None:
            href = search_results['href']
            url = SITE_URL + href
            driver.get(url)
            print("Success @ {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            logging.info("Success @ {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            return True
        
    #print("No spaces available @ {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    return False

if __name__ == "__main__":
    # Get settings
    data = yaml.safe_load(open("pwd.yaml"))
    SITE_URL = data['SITE_URL']
    LOGIN_URL = SITE_URL + "/registrar-student/sections/ViewSections.tap"
    CRAWL_URL = SITE_URL + "/registrar-student/sections/ViewSections.tap?service=direct&service=1&service=sectionsTable.sectionsTable.tableElement.tablePages.linkPage&sp=Asections%2FViewSections%2FsectionsTable.sectionsTable.tableElement.tableView&sp=2"
    USERNAME = data['username']
    PASSWORD = data['password']
    
    logging.basicConfig(filename='results.log', level=logging.INFO)
    target_elective = 'E326'
    target_stream = 4
    delay = 2
    log_delay = 5 #mins

    # Option 1: Run using Docker Chrome, suitable for remote (see README for instructions)
    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
    
    # Option 2: Run locally on Mac/PC with Firefox (needs geckodriver to be in PATH)
    #options = Options()
    #options.headless = True   # optional, running headless = False will allow you to see browser and actions 
    #driver = webdriver.Firefox(options=options)

    driver.get(LOGIN_URL)
    
    site_login()
    driver.get(CRAWL_URL)
    count = 0
    while not found_course(driver, target_elective, [target_stream]):
        count += 1
        site_refresh()
        sleep(delay)
        if count >= log_delay * 60 / delay:
            count = 0
            logging.info("Scraper running at {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
            #print("No spaces available @ {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        
    print("Program terminated")
        
        
    
