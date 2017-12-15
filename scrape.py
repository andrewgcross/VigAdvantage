# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:34:28 2017

@author: Andrew
"""

from datetime import datetime
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import sqlite3 #http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

class team():
    #def __init__(self):
    
    def set_name(self,name):
        self.name = name
    
    def set_link(self,link):
        self.link = link

class game():
    def __init__(self, html):
        self.html = html
                  
    def scrape_teams(self):
        cell = self.html.find('td') #should return the first column only
        self.tipOff = datetime.strptime(cell.span.text, '%m/%d  %I:%M %p').replace(year=datetime.now().year) #year (obviously) is not shown on the webpage
                
        teams = cell.find_all('a')
        self.teamAway = team()
        self.teamAway.set_name(teams[0].text)
        self.teamAway.set_link(teams[0].get('href'))
        
        self.teamHome = team()
        self.teamHome.set_name(teams[1].text)
        self.teamHome.set_link(teams[1].get('href'))

conn = sqlite3.connect('VigAdvantage.sqlite')
c = conn.cursor()

#Create the table
c.execute('CREATE TABLE IF NOT EXISTS :tn (:f1 :f1t, :f2 :f2t, :f3 :f3t, :f4 :f4t)', 
          {'tn':'GAMES', 
           'f1':'id', 'f1t':'INTEGER', 
           'f2':'tip', 'f2t':'DATETIME',
           'f3':'home', 'f3t':'TEXT',
           'f4':'away', 'f4t':'TEXT'})

url = "http://www.vegasinsider.com/college-basketball/odds/las-vegas/"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html5lib")

table = soup.find('table',class_='frodds-data-tbl')

#Deleting the unwanted tr's is the quickest and easiest short-term solution to filter out unwated rows
for delrow in table.find_all(class_="game-notes"):
    delrow.parent.decompose() #parent will identify the tr to be removed

rows = table.find_all('tr')

#Loop through every row on the main table, establishing a new object for every matchup
for row in rows:
    g = game(row)
    g.scrape_teams()
    
    
conn.commit()
conn.close()