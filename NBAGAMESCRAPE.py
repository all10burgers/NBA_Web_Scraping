import urllib
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlopen
import time
#test

#function to scrape game data for each year given. Incomplete function at the moment.
def scrape_year_data(years):
    #final_df = pd.DataFrame(columns=["Start(ET)", "Visitor", "VisitorPTS", "Home", "HomePTS", "OT", "Attend.", "Arena", "Notes"])


    for y in years:
        year = y

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games.html"

        html = urlopen(url)

        soup = BeautifulSoup(html, features="lxml")

        titles = [th.getText() for th in soup.findAll('thead', limit=1)[0].findAll('th')]

        headers = titles[0:9]

        rows = soup.findAll('tr')[1:]

        #game_stats["Date"] = [[th.getText() for th in rows[i].findAll('th')] for i in range(len(rows))]

        game_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

        #game_stats = [e for e in game_stats if e != []]

        game_stats2 = pd.DataFrame(game_stats, columns = headers)
        #game_stats2.drop("Date", axis=1, inplace=True)
        #game_stats2["Date"] = [[th.getText() for th in rows[i].findAll('th')] for i in range(len(rows))]


        #game_stats2.drop("Notes", axis=1, inplace=True)

        #final_df = final_df.append(game_stats2)




            

    print(game_stats2.info)
    game_stats2.to_csv("nba_game_data5.csv", index=False)

scrape_year_data(years=[1999])