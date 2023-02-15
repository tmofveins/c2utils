from fuzzywuzzy import fuzz
from pony.orm import * 

import re
import discord

import utils
import search.song as song
import search.chart as chart

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

#################################################

def display_search_result_as_embed(best_matches):
    if len(best_matches) == 0:
        return utils.generate_embed(
                    status = 'Error', 
                    msg = (
                        "No songs found. There could be an error with"
                        " your search or the bot."
                    )
                )

    if len(best_matches) == 1:
        return embed_single_match(best_matches[0])

    multiple_search_results = "\n".join(f"({match.song_id}) {match.title} / {match.artist}" 
                                for match in best_matches)

    return utils.generate_embed(
                    status = 'Error', 
                    msg = (
                        "Too many songs found. Please refine your search using the"
                        " full song title or song ID (in brackets).\n\n"
                        f"{multiple_search_results}"
                    )
            )

def embed_single_match(match):
    # generate appropriate discord embed for a single song match

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
    
    # since some charts are not available on the site but i want to display the
    # song difficulty regardless
    chart_strings = [f"{c.diff_name} {c.diff_level}" for c in charts]

    # include hyperlink if present, else take regular chart_string from chart_strings
    markdown_strings = [f"[{cs}]({c.diff_link})" if c.diff_link is not None 
                        else cs for cs, c in zip(chart_strings, charts)]

    return " | ".join(markdown_strings)