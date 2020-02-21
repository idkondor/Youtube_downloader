# Youtube_downloader
Script to extract mp3 from youtube videos

1. Install youtube-dl module
http://ytdl-org.github.io/youtube-dl/download.html

2. Download git repository
https://github.com/idkondor/Youtube_downloader.git

# Linux Systems
Run in the terminal:
python youtube_mp3_downloader.py -i "/home/user/Desktop/Youtube_script/Input_links.csv" -d "/home/user/Desktop/Youtube_script/Output_links.csv" -o "/home/user/Downloads/Youtube_downloader/"
"""
'-i' argument stands for '.csv' document in which links with youtube videos are stored
'-d ' argument stands for '.csv' document in which links with processed youtube videos need to be stored
'-o' argument stands for container directory where mp3 files will be saved 
