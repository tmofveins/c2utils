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

#################################################

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

#################################################


def get_table(SOURCE):
    """
    Scrapes the main table from the ct2viewer website. 
    
    :param SOURCE: ct2viewer site link
    :return: HTML table
    """

    try:
        r = requests.get(SOURCE, headers=utils.headers)
        c2v = BeautifulSoup(r.content, "lxml")

        if not os.path.exists("page.xml"):
            with open("page.xml", "w") as f:
                print(c2v.body, file=f)

        table = c2v.body.table.tbody

        return table

    except:
        return Exception("Unable to request from page.")


def parse_table(table):
    pass
    for song in table.find_all("tr"):
        return


#################################################

if __name__ == "__main__":
    table = get_table("https://ct2view.the-kitti.com/")
    parse_table(table)
