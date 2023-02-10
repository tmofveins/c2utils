import re

SOURCE = "https://ct2view.the-kitti.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

JP_REGEX = re.compile('[\u4E00-\u9FAF]|[\u3000-\u303F]|[\u3040-\u309F]|\
                    [\u30A0-\u30FF]\|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|\
                    [\u2605-\u2606]|[\u2190-\u2195]|\u203B')

# regex to detect emotes in user input
EMOTE_REGEX = re.compile("(:[a-zA-Z0-9_\-~]+?:)")

# regex to detect pings, channel titles, or roles
PING_REGEX = re.compile("<(#|@!|@#)\d+>")