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
        
    print("No spaces available @ {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    return False

if __name__ == "__main__":
    # Get settings
    data = yaml.safe_load(open("pwd.yaml"))
    SITE_URL = data['SITE_URL']
    LOGIN_URL = data['LOGIN_URL']
    CRAWL_URL = data['CRAWL_URL']
    USERNAME = data['username']
    PASSWORD = data['password']
    
    logging.basicConfig(filename='results.log', level=logging.INFO)
    target_elective = 'E326'
    target_stream = 4
    options = Options()
    options.headless = True    
    delay = 5
    log_delay = 5 #mins

    driver = webdriver.Firefox(options=options)
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
        
    print("Program terminated")
        
        
    
