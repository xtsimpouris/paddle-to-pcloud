from utils import loadSettings, saveSettings, cleanUp
from pcloud import PyCloud
import re
import requests
from datetime import datetime
import os

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

    x = re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2} ([0-9]+).*?\\..*", fname)
    if not x:
        continue

    fsize = file["size"]
    existing_files[x[1]] = {
        "name": fname,
        "size": fsize,
        "padlet_id": x[1],
    }

print("Identified %d files already in pCloud" % len(existing_files))

posts = {}
hash_id = "https://padlet.com/api/10/wishes?wall_hashid=%s&page_start=" % settings["padlet"]["wallid"]
while hash_id:
    print("Downloading %s ..." % hash_id)

    response = requests.get(hash_id)
    data = response.json()

    for wish in data.get("data", []):
        posts[ wish["id"] ] = wish

    if not data.get("meta", {}).get("next", False):
        break

    hash_id = "https://padlet.com/api/10/wishes?wall_hashid=%s&page_start=%s" % (settings["padlet"]["wallid"], data.get("meta", {}).get("next", False))

print("Let's start downloading")
for post_id in posts:
    post = posts[post_id]["attributes"]

    # File already exists
    if str(post.get("id", "")) in existing_files:
        continue

    created_at = datetime.strptime(post["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')

    title = cleanUp(post.get("body", ""))

    if not title:
        title = cleanUp(post.get("headline", ""))

    final_name = ("%s %s %s" % (created_at.strftime("%Y-%m-%d"), str(post.get("id", "")), title)).strip()
    final_name += "." + post["attachment_link"]["extension"]

    print("Downloading.. %s" % final_name, end = "")
    response = requests.get(post["attachment"])
    if response.status_code == 200:
        with open(final_name, "wb") as f:
            for chunk in response:
                f.write(chunk)
        print(" ..Done")
    else:
        print(" ..Error!!")
        continue

    print("Uploading.. %s" % final_name, end = "")
    response = pc.uploadfile(files=[final_name], path=settings["pcloud"]["folder"])
    if "error" in result:
        print(" ..Error!!")
    else:
        print(" ..Done")

    os.unlink(final_name)
