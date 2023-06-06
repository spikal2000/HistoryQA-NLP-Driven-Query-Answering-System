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
from selenium.common.exceptions import TimeoutException
import re
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException


def initialize_browser(n):
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get("https://flexbooks.ck12.org/user:zxbpc2rzcziwmthaz21hawwuy29t/cbook/world-history-studies_episd/")
    print("starting driver")
    wait = WebDriverWait(driver, 50)
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        try:
            click_button = wait.until(EC.element_to_be_clickable((By.ID, 'radix-'+str(n))))
            click_button.click()
            break
        except (TimeoutException, ElementNotInteractableException):
            continue
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

#________________Part2________________
def doc_link(new):
    url = "https://flexbooks.ck12.org/user:zxbpc2rzcziwmthaz21hawwuy29t/cbook/world-history-studies_episd"+ new
    return url

def extract_info(chapters):
    data = {}

    for i in range(0, len(chapters)):
    # for i in range(0, 1):
        for key in chapters[i].keys():
            with webdriver.Firefox(service=Service(GeckoDriverManager().install())) as driver:
                driver.set_page_load_timeout(60)# Set timeout to 30 seconds
                link = doc_link(chapters[i][key])
                try:
                    driver.get(link)
                except TimeoutException:
                    print("Loading took too much time!")
                    # Here you can also handle what to do if the page load takes too much time
                time.sleep(7)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                body_text = []
                
                body_text.append(soup.find_all(text=True))


                # p_elements = soup.find_all('p')
                # if p_elements is not None:
                #     body_text = [p.get_text() for p in p_elements]
                
                table_elements = soup.find_all('table')
                if table_elements is not None:
                    for table in table_elements:
                        rows = table.find_all('tr')
                        for row in rows:
                            cells = row.find_all('td')
                            for cell in cells:
                                body_text.append(cell.get_text())

                
                # d = soup.find('div', {'class': f"x-ck12-data-concept"})
                # table_content = []
                # body_text = []
                # if d is not None:
                #     ps = d.find_all('p')
                #     tables = soup.find_all('table')
                #     if ps is not None:
                #         for p in ps:
                #             body_text.append(p.get_text())
                #     if tables is not None:
                #         for table in tables:
                #             rows = table.find_all('tr')
                #             table_data = []
                #             for row in rows:
                #                 cells = row.find_all('td')
                #                 row_data = [cell.get_text() for cell in cells]
                #                 table_data.append(row_data)
                #             body_text.append(table_data)
                        
                # body_text = [tag.get_text() for tag in soup.body.descendants if tag.name]
                print("import data")
                print(body_text)
                match = re.match(r'(\d+\.\d+)\xa0\xa0(.*)', key)
                if match:
                    number, title = match.groups()
                    data[number] = {"title": title, "body_text": body_text}
    return data

# {x: {y :[]}}


def replace_pattern_in_urls(chapter_links_list, pattern):
    updated_links_list = []

    for chapter_links in chapter_links_list:
        updated_links = {}
        for chapter_name, url in chapter_links.items():
            # Substitute the pattern with an empty string
            url_clean = re.sub(pattern, '', url)
            updated_links[chapter_name] = url_clean
        updated_links_list.append(updated_links)

    return updated_links_list





#Get the chapters from the first page
# chapters = []
# for num, i in enumerate(range(1, 20, 2)):

#     driver = initialize_browser(i)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     parent = soup.find('div', {'id': f"course_item_child_{num+1}"})
#     chapters.append(get_links(parent))

# import pickle
# with open('chapters.pickle', 'wb') as handle:
#     pickle.dump(chapters, handle, protocol=pickle.HIGHEST_PROTOCOL)
import pickle

with open('chapters.pickle', 'rb') as handle:
    chapters = pickle.load(handle)


#clean the data
pattern = '/user:zxbpc2rzcziwmthaz21hawwuy29t/cbook/world-history-studies_episd'
# cleaned_chapters = replace_pattern_in_urls(chapters, pattern)


#iterate in the evry page and gather the data
# data = extract_info(cleaned_chapters)

# with open('data.pickle', 'wb') as s:
#     pickle.dump(chapters, s, protocol=pickle.HIGHEST_PROTOCOL)
with open('data.pickle', 'rb') as s:
    data = pickle.load(s)




