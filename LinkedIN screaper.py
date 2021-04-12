# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 08:10:27 2020

@author: archi
"""


# LinkedIN automated scraper

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome('C:/Users/archi/chromedriver/chromedriver.exe')
driver.get('https://www.linkedin.com')
time.sleep(0.5)

username = driver.find_element_by_class_name('input__input')
username.send_keys('unm')
password = driver.find_element_by_id('session_password')
password.send_keys('pw')

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
time.sleep(0.5)

driver.get('https://www.google.com')
time.sleep(0.5)


# For extracting profiles of people within search query          
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "HR" AND "India" AND "Microsoft"')
search_query.send_keys(Keys.RETURN)
time.sleep(0.5)

linkedin_urls = driver.find_elements_by_class_name('iUh30')
linkedin_urls = [url.text for url in linkedin_urls]



# Scraping Starts
from parsel import Selector
url = []
for urls in linkedin_urls:
    spl_word = ' › '
    res = urls.partition(spl_word)[2]
    if len(res)>5:
        if res!='...':
            main = 'https://in.linkedin.com/in/'
            urls = main+res
            url.append(urls)



names = []
jobs = []
companies = []
abouts = []
# For loop to iterate over each URL in the list
for linkedin_url in url:

   # get the profile URL 
   driver.get(linkedin_url)

   # add a 5 second pause loading each URL
   time.sleep(1)

   
   # assigning the source code for the webpage to variable sel
   sel = Selector(text=driver.page_source) 

   name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()
   if name:
    name = name.strip()
   names.append(name)
   
   job = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()
   if job:
    job = job.strip()
   jobs.append(job)
   
   company = sel.xpath('//*[starts-with(@class, "text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view")]/text()').extract_first()
   if company:
    company = company.strip()
   companies.append(company)
   
   about = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line")]/text()').extract_first()
   if about:
    about = about.strip()
   abouts.append(about)
            
df = pd.DataFrame(list(zip(names, jobs, companies, abouts, url)), columns =['Name','Job Title','Company','About', 'URL']) 
df.to_csv('scraped_data_linkedin.csv', index = False)

# terminates the application
driver.quit()