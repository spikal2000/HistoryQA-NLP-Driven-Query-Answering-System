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





def initialize_browser(num):
    driver.get("https://flexbooks.ck12.org/user:zxbpc2rzcziwmthaz21hawwuy29t/cbook/world-history-studies_episd/")
    print("starting driver")
    click_button = driver.find_element(by=By.ID, value='radix-'+num)
    click_button.click()

# setup driver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

initialize_browser("1")


soup = BeautifulSoup(driver.page_source, 'html.parser')

parent = soup.find('div', {'id': "course_item_child_1"})


chapter_links = {}

if parent:
    desired_elements = parent.find_all('a')
    for i in range(len(desired_elements)):
        chapter_links[desired_elements[i].text] = desired_elements[i]['href']
else:
    print("No parent element found.")



# # Now we can use BeautifulSoup to parse the HTML content
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# # Find the parent div
# parent = soup.find('div', {'class': "LevelItem__TextContainer-i60d4c-3 iQmFMO"})

# if parent:
#     desired_elements = parent.find_all('a')
#     print(desired_elements)
# else:
#     print("No parent element found.")

# # Remember to close the browser
# driver.quit()


# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# WebDriverWait(dr, 20).until(EC.element_to_be_clickable(By.XPATH, //button[@class='Accordion__StyledContent-z6hx9p-4 kbSByO']))