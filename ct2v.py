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
        song = Song.create_song_from_tr(tr)
        print(song)

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
