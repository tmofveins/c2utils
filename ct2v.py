from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from pykakasi import kakasi
from collections import Counter, defaultdict

import pandas as pd
import numpy as np
import requests
import re
import discord
import os

import utils
from song import Song 
from chart import Chart

#################################################

def get_table_from_soup(url):
    try:
        r = requests.get(url, headers=utils.headers)
        c2v = BeautifulSoup(r.content, "lxml")

        if not os.path.exists("table.xml"):
            with open("table.xml", "w") as f:
                print(c2v.body.table.prettify(), file=f)

        table = c2v.body.table

        return table

    except:
        return Exception("Unable to request from page.")

def parse_table_into_songs(table):
    curr_character = ""
    body = table.tbody

    with open ("out.txt", "w") as f:
        for tr in body.find_all("tr"):
            song, curr_character = Song.create_song_from_tr(tr, curr_character)
            print(song, file=f)
            print("\n---\n", file=f)

#################################################

if __name__ == "__main__":
    table = get_table_from_soup(utils.source_url)
    parse_table_into_songs(table)