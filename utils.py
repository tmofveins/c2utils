import re
from discord import Embed, Colour

SOURCE = "https://ct2view.the-kitti.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

JP_REGEX = re.compile('[\u4E00-\u9FAF]|[\u3000-\u303F]|[\u3040-\u309F]|\
                    [\u30A0-\u30FF]\|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|\
                    [\u2605-\u2606]|[\u2190-\u2195]|\u203B')

# regex to detect emotes/mentions/channels in user input
INVALID_INPUT_REGEX = "<(?::\w+:|@!*&*|#)[0-9]+>"

SONGS_ADDED_THIS_UPDATE = []

def generate_embed(status, msg):
    """
    Returns a Discord Embed with color depending on the message's status and custom error message.
    """
    colors = {
        "Error": Colour.dark_red(),
        "OK": Colour.dark_grey(),
        "Success": Colour.green(),
    }
    return Embed(title = status, colour = colors[status], description = msg)