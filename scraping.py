# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 11:54:07 2023

@author: spika
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC






def initialize_browser(n):
    # time.sleep(1)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get("https://flexbooks.ck12.org/user:zxbpc2rzcziwmthaz21hawwuy29t/cbook/world-history-studies_episd/")
    print("starting driver")
    # time.sleep(10)
    wait = WebDriverWait(driver, 15)
    # click_button = driver.find_element(by=By.ID, value='radix-'+str(n))
    click_button = wait.until(EC.presence_of_element_located((By.ID, 'radix-'+str(n))))
    click_button.click()
    return driver
    
def get_links(parent):

    time.sleep(1)
    chapter_links = {}

    if parent:
        desired_elements = parent.find_all('a')
        for i in range(len(desired_elements)):
            chapter_links[desired_elements[i].text] = desired_elements[i]['href']
    else:
        print("No parent element found.")
    
    return chapter_links





#1:{}
chapters = []
for num, i in enumerate(range(1, 20, 2)):

    driver = initialize_browser(i)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parent = soup.find('div', {'id': f"course_item_child_{num+1}"})
    chapters.append(get_links(parent))


