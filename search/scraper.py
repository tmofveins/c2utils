from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from pykakasi import kakasi
from pony.orm import *

import requests
import re
import discord
import os

import database
import utils
import search.song as song
import search.chart as chart

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

def compare_fuzz(song, best_matches, best_fuzz_ratio, fuzz_value):
    if fuzz_value > best_fuzz_ratio:
        best_matches.clear()
        best_matches.append(song)
        return True

    elif fuzz_value == best_fuzz_ratio:
        best_matches.append(song)
        return False

    return False

@db_session
def search_song(query):
    best_fuzz_ratio = 0
    best_matches = []

    for curr_song in select(curr_song for curr_song in song.Song):
        if curr_song.title.lower() == query.lower() or curr_song.song_id.lower() == query.lower():
            return [curr_song]

        fuzz_value = fuzz.token_set_ratio(curr_song.title, query)

        if compare_fuzz(curr_song, best_matches, best_fuzz_ratio, fuzz_value):
            best_fuzz_ratio = fuzz_value 

    # if there are no good matches, return nothing
    if best_fuzz_ratio < 0.2:
        return []

    return best_matches

def show_search_results_print(best_matches):
    for match in best_matches:
        print(f"({match.song_id}) {match.title} - {match.artist}")

def show_search_results_embed(best_matches):
    if len(best_matches) == 0:
        return utils.generate_embed(
                    status = 'Error', 
                    msg = (
                        "No songs found. There could be an error with"
                        " your search or the bot."
                    )
                )

    if len(best_matches) == 1:
        return embed_search_result(best_matches[0])

    return utils.generate_embed(
                    status = 'Error', 
                    msg = (
                        "Too many songs found. Please refine your search using the full song title"
                        " or song ID (in brackets).\n"
                        f"{show_search_results_print(best_matches)}"
                    )
            )

def embed_search_result(match):
    embed = discord.Embed(colour = discord.Colour.green())

    song_jacket = utils.SOURCE + "thumbnail/" + match.song_id + ".png"
    embed.set_thumbnail(url = song_jacket)

    embed.add_field(name = f"{match.title}", value = f"{match.artist}", inline = False)
    embed.add_field(name = "BPM", value = f"{match.bpm}", inline = True)
    embed.add_field(name = "Character", value = f"{match.character}", inline = True)

    difficulty_string = get_difficulty_string(match)
    embed.add_field(name = "Difficulty", value = difficulty_string, inline = False)
    
    embed.set_footer(text = "Taken from ct2view.the-kitti.com")
 
    return embed

def get_difficulty_string(match):
    charts = chart.retrieve_charts_for_song(match)

    difficulty_string = ""

    if charts[0].diff_link is not None:
        difficulty_string += f"[{charts[0].diff_name} {charts[0].diff_level}]({charts[0].diff_link})"
        difficulty_string += " | "

    if charts[1].diff_link is not None:
        difficulty_string += f"[{charts[1].diff_name} {charts[1].diff_level}]({charts[1].diff_link})"
        difficulty_string += " | "

    difficulty_string += f"[{charts[2].diff_name} {charts[2].diff_level}]({charts[2].diff_link})"

    if charts[3].diff_link is not None:
        difficulty_string += " | "
        difficulty_string += f"[{charts[3].diff_name} {charts[3].diff_level}]({charts[3].diff_link})"

    if charts[4].diff_link is not None:
        difficulty_string += " | "
        difficulty_string += f"[{charts[4].diff_name} {charts[4].diff_level}]({charts[4].diff_link})"

    print(f"DIFF: {difficulty_string}")
    
    return difficulty_string

#################################################