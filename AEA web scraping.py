# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:29:37 2020

@author: Bo Klauth
"""

# getting website
import requests
# What does it do?
import lxml.html as lh
# beautiful soup
import bs4 as bs
# pandas for data wranging
import pandas as pd

#import lxml.html as lh
# This is another way with start session and page navigation
# start session
session = requests.Session()

### the url is the desired site that the web redirect too after log in
url='https://www.eval.org/l/li/in/'
# login with hidden login
login = session.get(url)
login_html = lh.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
payload = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
print(payload)

# create the payload
payload={'uname':'youremail@domain', 
        'pass':'yourpassword'
        }
# PASSWORD ARE NOT PROTECTED HERE
# post payload to the website log in

s = session.post("https://www.eval.org/l/li/in/", data=payload)

# navigate to the next page
s = session.get('https://www.eval.org/p/es/vo/eid=42&etid=834')
soup=bs.BeautifulSoup(s.text, 'html.parser')
soup

# get the links to the proposed sesssions, which will use javascript function to go to votes
print('--Links to Conference Sessions--')
temp_col=[]
temp_link=[]
# Find the first five cite elements with a citation class
cites = soup.find_all('td', class_='so_normal')
for x in cites:
    print(x.get_text())
    each_temp_col=x.get_text()
    temp_col.append(each_temp_col)
    # Inside of this cite element, find the first a tag    
    if x.find('a'):
        link=x.find('a')
        base_href="https://www.eval.org/"
    # ... and show its URL
        print(base_href+link.get('href'))
        each_temp_link=base_href+link.get('href')
        temp_link.append(each_temp_link)
    else:
        no_link="no link"
        each_temp_link=no_link
        temp_link.append(each_temp_link)
        print()
        
temp_df=pd.DataFrame({'col1':temp_col, 'col2':temp_link})
# ({'Product Name':products,'Price':prices})
temp_df

# print only the link for the proposed session
url_list=[]
for i in range(0, len(temp_link), 5):
#     print(i, temp_link[i])
    url_item=temp_link[i]
    url_list.append(url_item)
url_list

# get proposed session id
sid=[]
for i in range(0, len(url_list)):
    sid_item=url_list[i].split("sid=")[1].split('&etid')[0]
    sid.append(sid_item)
print(sid)

# note that after spliting, you have two items, 
# and you have to use the index number to get what you want

# an example
# name = 'Braund, Mr. Owen Harris'
# first_name = name.split('.')[1].lstrip().split(' ')[0]
# first_name

len(url_list)
print(url_list[0])
print(url_list[1])
print(url_list[2])

import numpy

# It has some delay while processing the information
# it would be a good practice to store the information
# need to store the web infomation
# range later can be replaced by len(url_list), which equals 27
print("url_list", len(url_list))
url_storage=[]
for url_index in range(0, len(url_list)):
    url=url_list[url_index]
    s=session.get(url)
    soup=bs.BeautifulSoup(s.text, 'html.parser')
    url_storage.append(soup)

# use storage to prevent from having an account lock issue while testing
# len(url_storage)
# url_storage
# writing as file
html_page=pd.DataFrame(url_storage)
html_page.to_csv(r"C:\Users\Dell\Documents\00_Python Programming\practice data\dup_vote_pages.csv", index=False)

# LIMIT THE LINKS PER MINUTE OR YOU ARE LOCKED OUT

# navigate to the next page
# s = session.get('https://www.eval.org/p/es/vo/eid=42&etid=834')
# create data frame columsn

###### block 1########
session_id=[]
sid_link=[]
Evaluator=[]
uid=[]
Vote=[]

# 1 iterate through links
# range later can be replaced by len(url_list), which equals 27
# for url_index in range(0, len(url_list)):
#     url=url_list[url_index]
#     s=session.get(url)
#     soup=bs.BeautifulSoup(s.text, 'html.parser')

for url_index in range(0,len(url_storage)):
    url_content=url_storage[url_index]
    soup=url_content

    # 2 iterate to get vote tables within each link
    # Need to do this for every link
    vote_tables=[]
    uid_list=[]
    vote_content=soup.find_all('td', class_='so_normal')
    for x in vote_content:
    #     print(x.get_text())
        vote_tables.append(x.get_text())
    # get uid from vote_content
        if x.find('a'):
            link=x.find('a')
        
            # ... and show its URL
            # print(link.get('href'))
            each_uid=link.get('href')
            uid_list.append(each_uid)
        else:
            no_link="no link"
            each_uid=no_link
            uid_list.append(each_uid)
        # print()
    # get all uid per iteration of url
    # use n of len(uid_list)-1 to prevent out of range error
    
    # 
    for i in range(0, len(uid_list)-1, 3):
        uid_per_url=uid_list[i+1]
        uid.append(uid_per_url)
    # spliting the link and get id
    
    
        
        # 3: iterate within each vote_table to append Evaluators and Vote
        # select data
        
    for y in range(0, len(vote_tables)-1, 3):
        # evaluator
        eva_item=vote_tables[y+1]
        Evaluator.append(eva_item)
        # vote
        vote_item=vote_tables[y+2]
        Vote.append(vote_item)
        # session id
        session_id_per_url=sid[url_index]
        session_id.append(session_id_per_url)
        # session link
        session_link_per_url=url_list[url_index]
        sid_link.append(session_link_per_url)
    #     print(Evaluator, Vote)
        

####### end block 1 #######
        
eval_id=[]
for i in range(0, len(uid)):
    eval_id_1=uid[i].split("uid=")[1]
    eval_id.append(eval_id_1)


df=pd.DataFrame({"sid": session_id, "sid_link": sid_link, "evaluator": Evaluator, "eval_id": eval_id, "vote": Vote})
df


df1=df.drop(columns=['evaluator'])

# temp_eval_id=pd.crosstab(index=df['eval_id'],  # Make a crosstab
#                               columns="count")      # Name the count column)
# temp_eval_id[0]

# # make a data format with raters as columns
# convert character to numeric
df['vote']=pd.to_numeric(df.vote)
df.dtypes
df2=df[['sid', 'eval_id', 'vote']]

# check datatype
df.dtypes

# convert to wide format
df3=df2.pivot_table(index=['sid'], 
                   columns=['eval_id'], 
                   values=['vote'])
    
df3

df3=df3.reset_index()

cols=df3.columns
cols
df3

cols.get_level_values(1)
cols.get_level_values(0)
l1=cols.get_level_values(1)
l0=cols.get_level_values(0)
names=[x[1] if x[1] else x[0] for x in zip(l0, l1)]
names
df3.columns=names
df3

# print(df3.add_prefix('X_'))
df4=df3.add_prefix('rater_')
df4.rename(columns={'rater_sid':'sid'}, inplace=True)
df4

# write a csv file out
df.to_csv(r'C:\Users\Dell\Documents\00_Python Programming\practice data\2020_eval_dup_scores.csv', index=False)
df4.to_csv(r'C:\Users\Dell\Documents\00_Python Programming\practice data\2020_eval_dup_raters_scores.csv', index=False)
