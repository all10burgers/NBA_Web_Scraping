import urllib
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlopen

#function to scrape nba team statistics over years given as arguments
def scrape_Team_Data(years):

    final_df = pd.DataFrame(columns=["Year", "Team", "Win", "Loss", "W/L%", "GB", "PS/G", "PA/G", "SRS", "Playoffs", "Losing_Season"])

    for y in years:

        year = y

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

        html = urlopen(url)

        soup = BeautifulSoup(html, features="lxml")

        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

        headers = titles[1:titles.index("SRS")+1:]

        titles = titles[titles.index("SRS")+1:]

        try:
            row_titles = titles[0:titles.index("Eastern Conference")]
        except: row_titles = titles

        for i in headers:
            row_titles.remove(i)
        row_titles.remove("Western Conference")
        divisions = ["Atlantic", "Central", "Southeast", "Northwest", "Pacific", "Southwest", "Midwest"]

        for d in divisions:
            try:
                row_titles.remove(d)
            except:
                print("No Division:", d)

        rows = soup.findAll('tr')[1:]

        team_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

        team_stats = [e for e in team_stats if e != []]

        team_stats = team_stats[0:len(row_titles)]
        # add team name to each row in team_stats
        for i in range(0, len(team_stats)):
            team_stats[i].insert(0, row_titles[i])
            team_stats[i].insert(0, year)
            
        # add team, year columns to headers
        headers.insert(0, "Team")
        headers.insert(0, "Year")
        
        # create a dataframe with all aquired info
        year_standings = pd.DataFrame(team_stats, columns = headers)
        
        # add a column to dataframe to indicate playoff appearance
        year_standings["Playoffs"] = ["Y" if "*" in ele else "N" for ele in year_standings["Team"]]
        # remove * from team names
        year_standings["Team"] = [ele.replace('*', '') for ele in year_standings["Team"]]
        # add losing season indicator (win % < .5)
        year_standings["Losing_season"] = ["Y" if float(ele) < .5 else "N" for ele in year_standings["W/L%"]]
        
        # append new dataframe to final_df
        final_df = final_df.append(year_standings)
        
    # print final_df
    print(final_df.info)
    # export to csv
    final_df.to_csv("nba_team_data.csv", index=False)




scrape_Team_Data(years=[1999, 2000, 2001, 2002])


