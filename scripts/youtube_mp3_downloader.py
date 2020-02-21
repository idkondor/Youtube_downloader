from __future__ import unicode_literals
import youtube_dl
import secrets
import time
import random
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-i", "--docIn", dest="pathToDoc", help="Input folder path with links!")
parser.add_argument("-o", "--dirOut", dest="pathOutput", help="Input folder path to download!")
parser.add_argument("-d", "--docOut", dest="pathToDocOut", help="Input folder path for output links!")
args = parser.parse_args()
pathToDoc = args.pathToDoc
pathOutput = args.pathOutput
pathToDocOut = args.pathToDocOut


class ErrorHandler(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def destination_control(link_type, gender, language):
    path = link_type + '/' + gender + '/' + language + '/'
    if link_type == "Noise":
        return link_type + "/"
    else:
        return path


def downloading_status(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


with open(pathToDoc) as linksFile:
    linksDataType = linksFile.readline()
    linksDataContainer = linksFile.read()
    linksList = linksDataContainer.splitlines()
    linksDictionaryList = []
    for link in linksList:
        linksDictionaryList.append(dict(zip(linksDataType.split(","), link.split(","))))

linksSheet = open(pathToDocOut, "r+")
linksSheet.write("URL, Type, Gender, Language, Duration, Comments, Availability, MD5" + "\n")

for dictionaryLink in linksDictionaryList:
    print(dictionaryLink)
    hashName = secrets.token_hex(nbytes=16)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': ErrorHandler(),
        'progress_hooks': [downloading_status],
        'noplaylist': True,
        'outtmpl': pathOutput + destination_control(dictionaryLink["Type"], dictionaryLink["Gender"],
                                                    dictionaryLink["Language"]) + hashName + '.%(ext)s'
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([dictionaryLink["URL"]])
            dictionaryLink["Availability"] = "Valid"
    except:
        dictionaryLink["Availability"] = "INVALID!"
    linksDictValues = []
    dictItems = dictionaryLink.items()
    for value in dictItems:
        if value[0] == "MD5\n":
            linksSheet.write(hashName + "\n")
            break
        linksSheet.write(value[1] + ", ")
    time.sleep(random.randint(10, 30))

linksSheet.close()
