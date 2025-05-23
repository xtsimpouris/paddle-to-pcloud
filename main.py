from utils import loadSettings, saveSettings
from pcloud import PyCloud
import re

settings = loadSettings()

try:
    pc = PyCloud(settings["pcloud"]["email"], settings["pcloud"]["password"], endpoint=settings["pcloud"]["endpoint"])
except:
    print("Unable to login to pCloud, are credentials correct?")

    # Force request credentials next time
    del settings["pcloud"]["email"]
    del settings["pcloud"]["password"]
    del settings["pcloud"]["endpoint"]
    saveSettings(settings)

    exit()

result = pc.listfolder(path=settings["pcloud"]["folder"])
if "error" in result:
    print("pCloud folder '%s' is not valid, please provide a valid one" % settings["pcloud"]["folder"])

    # Force request folder next time
    del settings["pcloud"]["folder"]
    saveSettings(settings)

    exit()

existing_files = {}
for file in result["metadata"]["contents"]:
    fname = file["name"]

    # 2025-01-30 3309877743 Η ομάδ
    x = re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2} ([0-9]+) .*", fname)
    if not x:
        continue

    fsize = file["size"]
    existing_files[x[1]] = {
        "name": fname,
        "size": fsize,
        "paddle_id": x[1],
    }

print("Identified %d files already in pCloud" % len(existing_files))
