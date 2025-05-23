from yaml import safe_load, dump
from getpass import getpass
import re

SETTINGS_FILENAME = "settings.yaml"

def loadSettings():
    settings = {}
    try:
        with open(SETTINGS_FILENAME, 'r') as file:
            settings = safe_load(file)
    except:
        pass

    if "pcloud" not in settings:
        settings["pcloud"] = {}

    if "email" not in settings["pcloud"] or settings["pcloud"]["email"].strip() == "":
        email = input("Please provide email for pCloud: ")
        settings["pcloud"]["email"] = email.strip()

    if "password" not in settings["pcloud"] or settings["pcloud"]["password"].strip() == "":
        password = getpass("Please provide password for pCloud: ")
        settings["pcloud"]["password"] = password.strip()

    if "folder" not in settings["pcloud"] or settings["pcloud"]["folder"].strip() == "":
        folder = input("Please provide folder for pCloud: ")
        settings["pcloud"]["folder"] = folder.strip().rstrip("/")

    if "endpoint" not in settings["pcloud"] or settings["pcloud"]["endpoint"].strip() == "":
        endpoint = input("Please provide endpoint for pCloud (eapi or api): ")
        settings["pcloud"]["endpoint"] = endpoint.strip()

    if "paddle" not in settings:
        settings["paddle"] = {}

    if "wallid" not in settings["paddle"] or settings["paddle"]["wallid"].strip() == "":
        wallid = input("Please provide wallid for paddle: ")
        settings["paddle"]["wallid"] = wallid.strip()

    saveSettings(settings)
    return settings

def saveSettings(settings):
    with open(SETTINGS_FILENAME, 'w') as file:
        dump(settings, file, allow_unicode=True)

def cleanUp(t, max_len = 100):
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    t = tag_re.sub('', t)

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
    "]+", re.UNICODE)
    t = emoji_pattern.sub('', t)

    t = t.replace("/", "..")
    t = t.replace("\\", "..")
    t = t.replace("!", ", ")
    t = t.replace("?", ", ")
    t = t.replace(":", ", ")
    t = t.replace('”', " ")
    t = t.replace('"', " ")
    t = t.replace('»', " ")
    t = t.replace('«', " ")
    t = t.replace(';', ", ")
    t = t.replace('⁉', ", ")
    t = t.replace('“', " ")

    t = t.replace('.', " . ")
    t = t.replace(',', " , ")
    t = t.replace('(', " ( ")
    t = t.replace(')', " ) ")
    t = t.replace('⏰', " ")
    t = t.replace('—', " - ")
    t = t.replace('-', " - ")


    t = t.strip()   
    t = t.rstrip(".")
    t = t.rstrip(",")

    parts = t.split(" ")
    t = ""
    for part in parts:
        part = part.strip()
        if part == "":
            continue

        if part == "." or part == ",":
            t = t + part
        else:
            t = t + " " + part

        t = t.replace(',,', ",")
        t = t.replace('( ', "(")
        t = t.replace(' )', ")")

        if len(t) > max_len:
            break

    t = t.rstrip(".")
    t = t.rstrip(",")
    return t.strip()
