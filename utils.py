from yaml import safe_load, dump
from getpass import getpass

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
