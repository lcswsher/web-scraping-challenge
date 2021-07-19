#!/usr/bin/env python
# coding: utf-8

# ## Dependencies

# In[1]:


# Dependencies
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import pymongo
import datetime
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:

def init_browser():
    # to setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News - Scrape the Mars News Site and collect the latest News Title and Paragraph Text

# In[3]:

# mars_information = {}

def scrape():
    browser = init_browser()
    
    #------------------ MARS NEWS-----------------------------
    
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # In[4]:
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # In[5]:

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

   
    # ------------------ JPL Mars Space Images - Featured Image ---

    # In[6]:

    
    # URL of page to be scraped
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)


    # In[7]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup_JPL = BeautifulSoup(html, 'html.parser')


    # In[8]:


    # identify and return the url string for the featured_image_url 
    image_path = soup_JPL.find_all('img')[1]['src']
    featured_image_url = url2 + image_path
    print(featured_image_url)


    # ## MARS Facts - Table Mars facts including diameter, mass, etc

    # In[9]:

    
    # We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
    url3 = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url3)
    table = tables[1]
    table.columns = ['Mars Planet Profile', "Dimentions"]
    Mars_Table = table.drop(index=0)
    Mars_Table.set_index('Mars Planet Profile', inplace=True)
    Mars_Table


    # In[10]:


    # comparison table converted from dataframe to html table (note: all "\n" - unwanted news lines, have been dropped from html table)
    html_table = Mars_Table.to_html()
    clean_html_table = html_table.replace('\n', '')
    print(clean_html_table)


    # In[11]:


    # Saving the Mars Earth Comparison table directly to an HTML table string called "table.html"
    Mars_Table_HTML = Mars_Table.to_html('table.html')


    # In[12]:


    # to print out html saved to file - "table.html"
    Mars_Table_HTML = Mars_Table.to_html()
    print(Mars_Table_HTML)


    # ## MARS Hemispheres

    # In[13]:


    url_hemisphere = "https://marshemispheres.com"
    browser.visit(url_hemisphere)
    html_hemisphere = browser.html
    soup = BeautifulSoup (html_hemisphere, "html.parser")


    # In[14]:


    hemispheres = soup.find_all("div", class_="item")
    hemispheres_info = []
    hemispheres_url = "https://marshemispheres.com/"

    for i in hemispheres:
        title = i.find("h3").text
        hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        web_info = BeautifulSoup(image_html, "html.parser")
        
        # Create full image url
        img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
        
        hemispheres_info.append({"title" : title, "img_url" : img_url})


    # In[15]:


        hemispheres_info


    # In[16]:
    
    #Dictionary 
    mars_information = {"News_Title": news_title, "News_Article": news_p,
                        "Featured_Image": featured_image_url, "Facts_Table": Mars_Table_HTML,
                        "Hemisphere_Images": hemispheres_info}

    browser.quit()

    return mars_information

# print(mars_information)
