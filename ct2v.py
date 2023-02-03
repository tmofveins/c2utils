from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from pykakasi import kakasi
from collections import Counter, defaultdict

import pandas as pd
import numpy as np
import requests
import re
import discord
import logging
import http.client
import utils
import os

from song import Song 
from chart import Chart

#################################################

# debug stuff for requests
"""
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
"""

#################################################


def get_table_from_soup(URL):
    try:
        r = requests.get(URL, headers=utils.headers)
        c2v = BeautifulSoup(r.content, "lxml")

        if not os.path.exists("table.xml"):
            with open("table.xml", "w") as f:
                print(c2v.body.table.prettify(), file=f)

        table = c2v.body.table

        return table

    except:
        return Exception("Unable to request from page.")

def parse_table(table):
    headers = table.thead
    body = table.tbody

    split_table_by_characters(headers, body)

def split_table_by_characters(headers, body):
    #character_songs = []
    curr_character = ""

    for tr in body.find_all("tr"):
        # go through each td and get the corresponding data, in sequence
        iterator = iter(tr.find_all("td"))
        
        td = next(iterator)

        if td.has_attr("rowspan"):
            curr_character = td.text
            
            # another iteration to also get the song title
            td = next(iterator)
            title = td.text

        else:
            title = td.text

        td = next(iterator)
        artist = td.text

        td = next(iterator)
        bpm = td.text

        charts = []

        td = next(iterator)
        easy_lv = td.text
        easy_link = ""
        if td.find('a'):
            easy_link = td.a.text
        easy_chart = Chart("EASY", easy_lv, easy_link)
        charts.append(easy_chart)

        td = next(iterator)
        hard_lv = td.text
        hard_link = ""
        if td.find('a'):
            hard_link = td.a.text
        hard_chart = Chart("HARD", hard_lv, hard_link)
        charts.append(hard_chart)

        td = next(iterator)
        chaos_lv = td.text
        chaos_link = ""
        if td.find('a'):
            chaos_link = td.a.text
        chaos_chart = Chart("CHAOS", chaos_lv, chaos_link)
        charts.append(chaos_chart)

        song = Song("", curr_character, title, artist, bpm, charts)
        print(song)
        
        """
        # check for glitch chart
        td = next(iterator)
        if
        glitch_lv = td.text
        glitch_link = ""
        if td.find('a'):
            glitch_link = td.a.text
        glitch_chart = chart.Chart("GLITCH", glitch_lv, glitch_link)

        # check for special chart (i.e. crash/drop/dream)
        td = next(iterator)
        sp_lv = td.text
        sp_link = ""
        if td.find('a'):
            sp_link = td.a.text
        easy_chart = chart.Chart("EASY", easy_lv, easy_link)"""

        return



def get_df_from_html(source):
    charts_df = pd.read_html(source, encoding = "UTF-8", header = 0, flavor = ["lxml"])
    charts_df = pd.concat(charts_df)
    charts_df = charts_df[charts_df['Song'].notna()]

    if not os.path.exists("table.csv"):
        charts_df.to_csv("table.csv")
    
    #print(charts_df[~charts_df["Unnamed: 9"].isnull()])

#################################################

if __name__ == "__main__":
    table = get_table_from_soup("https://ct2view.the-kitti.com/")
    parse_table(table)
    #get_df_from_html("https://ct2view.the-kitti.com/")
