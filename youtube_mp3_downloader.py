from __future__ import unicode_literals
import youtube_dl
import secrets
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-i", "--docIn", dest="pathToDoc", help="Input folder path with links!")
parser.add_argument("-o", "--dirOut", dest="pathOutput", help="Input folder path to download!")
parser.add_argument("-d", "--docOut", dest="pathToDocOut", help="Input folder path for output links!")
args = parser.parse_args()
pathToDoc = args.pathToDoc
pathOutput = args.pathOutput
pathToDocOut = args.pathToDocOut


class MyLogger(object):
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


def my_hook(d):
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

for youtube_link in linksDictionaryList:
    print(youtube_link)
    hashName = secrets.token_hex(nbytes=16)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'noplaylist': True,
        'outtmpl': pathOutput + destination_control(youtube_link["Type"], youtube_link["Gender"],
                                                    youtube_link["Language"]) + hashName + '.%(ext)s'
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_link["URL"]])
            youtube_link["Availability"] = "Valid"
    except:
        youtube_link["Availability"] = "INVALID!"
    linksDictValues = []
    dictItems = youtube_link.items()
    for value in dictItems:
        if value[0] == "MD5\n":
            linksSheet.write(hashName + "\n")
            break
        linksSheet.write(value[1] + ", ")

linksSheet.close()
