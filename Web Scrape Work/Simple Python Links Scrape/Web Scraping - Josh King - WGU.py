#!/usr/bin/env python
# coding: utf-8

# In[70]:


from bs4 import BeautifulSoup
import requests
import re
import csv


# In[71]:


url = 'http://www.census.gov/programs-surveys/popest.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# In[72]:


links_list = []

for tag in soup.find_all('a', href=True):
    
    link = tag.get('href').rstrip('/')
    
    if bool(re.search('[^\/]\/[^\/].*\....$', link)) and not link.endswith('.htm'):
        continue
    elif link.startswith('#'):
        continue
    elif link == "":
        continue
    elif link.startswith('/'):
        link = "https://www.census.gov" + link
        
    links_list.append(link)


# In[73]:


links_nodupes = list(set(links_list))
print(links_nodupes)


# In[74]:


with open('Josh Webscrape WGU.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(links_nodupes)


# In[ ]:




