from bs4 import BeautifulSoup

import requests

import utils
from search import song
from search import chart

#################################################

def get_table_from_soup():
    try:
        r = requests.get(utils.SOURCE, headers = utils.HEADERS)
        c2v = BeautifulSoup(r.content, "lxml")
        table = c2v.body.table
        
        return table

    except:
        return Exception("Unable to request from page.")

def parse_table_into_songs(table):
    curr_character = ""
    body = table.tbody

    for tr in body.find_all("tr"):
        curr_character = create_song_from_tr(tr, curr_character)

#################################################

def create_song_from_tr(tr, curr_character):
    iterator = iter(tr.find_all("td"))
    td = next(iterator)

    if td.has_attr("rowspan"):
        curr_character = td.text 

        # another iteration to also get the song title
        td = next(iterator)
        title = td.text
    else:
        title = td.text

    # no title, no song
    if title == "":
        return ""

    td = next(iterator)
    artist = td.text

    td = next(iterator)
    bpm = td.text

    td = next(iterator)
    _, (easy_name, easy_diff, easy_link) = create_chart_from_td(td, "EASY")

    td = next(iterator)
    _, (hard_name, hard_diff, hard_link) = create_chart_from_td(td, "HARD")

    # song_id is only guaranteed obtainable from the chaos chart
    td = next(iterator)
    song_id, (chaos_name, chaos_diff, chaos_link) = create_chart_from_td(td, "CHAOS")

    td = next(iterator)
    _, (glitch_name, glitch_diff, glitch_link) = create_chart_from_td(td, "GLITCH")

    td = next(iterator)
    _, (sp_name, sp_diff, sp_link) = create_chart_from_td(td, "SPECIAL")

    song.add_song_to_db(song_id, curr_character, title, artist, bpm)
    chart.add_chart_to_db(song_id, easy_name, easy_diff, easy_link)
    chart.add_chart_to_db(song_id, hard_name, hard_diff, hard_link)
    chart.add_chart_to_db(song_id, chaos_name, chaos_diff, chaos_link)

    if glitch_diff is not None:
        chart.add_chart_to_db(song_id, glitch_name, glitch_diff, glitch_link)

    if sp_diff is not None:
        chart.add_chart_to_db(song_id, sp_name, sp_diff, sp_link)

    return curr_character

def create_chart_from_td(td, diff_name):
    chart_lv = td.text

    # no level, no chart
    if chart_lv == "":
        return "", (None, None, None)

    chart_link = ""
    if td.find('a'):
        chart_link = td.a.get('href')

    song_id = ""

    # chaos chart is always present, hence song_id only obtainable from here
    if diff_name == "CHAOS":
        song_id = chart_link.split("/")[-2]
    # crash/drop/dream is stored in the same table space, so we use url to determine which it is
    elif diff_name == "SPECIAL":
        diff_name = chart_link.split("/")[-1]

    return song_id, (diff_name, chart_lv, chart_link)

#################################################

def update_database():
    table = get_table_from_soup()
    parse_table_into_songs(table)

    num_songs_added = len(utils.SONGS_ADDED_THIS_UPDATE)
    songs_added_blurb = "\n".join(s for s in utils.SONGS_ADDED_THIS_UPDATE)

    utils.SONGS_ADDED_THIS_UPDATE = []

    return num_songs_added, songs_added_blurb

def add_trans_title(song_id, trans_title):
    return song.add_trans_title(song_id, trans_title)