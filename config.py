import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", "23392712"))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
API_HASH = getenv("API_HASH", "7cb236b197b25c243fa83e7e0173d0e6")

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "")

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "")

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 5400))

# Song download limit duration
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "5400"))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", ""))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Get this value from @L2R_KING on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "5820831398"))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/IstkharXrobot/Bwf")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv("GIT_TOKEN", None)  # Fill this variable if your upstream repository is private

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/https://t.me/+DWd9sVKOFakwMTBl")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/https://t.me/+DWd9sVKOFakwMTBl")

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Automatically leave chat if enabled
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "False")
AUTO_SUGGESTION_TIME = int(getenv("AUTO_SUGGESTION_TIME", "5400"))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Spotify API credentials
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "bcfe26b0ebc3428882a0b5fb3e872473")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "907c6a054c214005aeae1fd752273cc4")

# Maximum limit for fetching playlist's track
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Time limits and cleanup
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "5"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━
# Pyrogram sessions
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━

# Validate URLs
def validate_url(url: str):
    if not re.match(r'^(https?://)', url):
        raise SystemExit(f"[ERROR] - Your URL {url} is invalid. Please ensure it starts with https://")

# Validate support channel and chat URLs
if SUPPORT_CHANNEL:
    validate_url(SUPPORT_CHANNEL)

if SUPPORT_CHAT:
    validate_url(SUPPORT_CHAT)

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━

# Utility function to convert time in HH:MM format to seconds
def time_to_seconds(time):
    parts = time.split(":")
    return sum(int(parts[i]) * 60 ** (len(parts) - 1 - i) for i in range(len(parts)))

# Convert duration limits to seconds
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

# ━━━━━━━━━━━━━❖ ➥ 𝐿2𝙍 𝗠𝗨𝗦𝗜𝗖™🇮🇳━━━━━━━━━━━

# Initialize other variables
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
chatstats = {}
userstats = {}
clean = {}

# Set default images
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/e576aa8308c49d945f433.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/e576aa8308c49d945f433.jpg")
PLAYLIST_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
STATS_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/e576aa8308c49d945f433.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra"
