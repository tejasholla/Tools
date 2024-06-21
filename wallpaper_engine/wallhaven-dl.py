import os
import getpass
import re
import requests
import urllib
import json

# Determine the path to the Pictures directory and create the Wallpapers folder if it doesn't exist
pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
wallpapers_dir = os.path.join(pictures_dir, "Wallpapers")
os.makedirs(wallpapers_dir, exist_ok=True)

BASEURL = "https://wallhaven.cc/api/v1/w/"
cookies = dict()

global APIKEY
APIKEY = ""

def category():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallpapers only.
    ga      - For 'General' and 'Anime' wallpapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ').lower()
    ctags = {'all': '111', 'anime': '010', 'general': '100', 'people': '001', 'ga': '110', 'gp': '101'}
    ctag = ctags[ccode]

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw': '100', 'sketchy': '010', 'nsfw': '001', 'ws': '110', 'wn': '101', 'sn': '011', 'all': '111'}
    ptag = ptags[pcode]

    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + "&categories=" + \
              ctag + '&purity=' + ptag + '&page='

def latest():
    global BASEURL
    print('Downloading latest')
    topListRange = '1M'
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&topRange=' + \
              topListRange + '&sorting=toplist&page='

def search():
    global BASEURL
    query = input('Enter search query: ')
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&q=' + \
              urllib.parse.quote_plus(query) + '&page='

def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    urlreq = requests.get(url, cookies=cookies)
    pagesImages = json.loads(urlreq.content)
    pageData = pagesImages["data"]

    for i in range(len(pageData)):
        currentImage = (((pageId - 1) * 24) + (i + 1))

        url = pageData[i]["path"]

        filename = os.path.basename(url)
        osPath = os.path.join(wallpapers_dir, filename)
        if not os.path.exists(osPath):
            imgreq = requests.get(url, cookies=cookies)
            if imgreq.status_code == 200:
                print("Downloading : %s - %s / %s" % (filename, currentImage, totalImage))
                with open(osPath, 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
            elif imgreq.status_code != 403 and imgreq.status_code != 404:
                print("Unable to download %s - %s / %s" % (filename, currentImage, totalImage))
        else:
            print("%s already exists - %s / %s" % (filename, currentImage, totalImage))

def main():
    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "search" for downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['category', 'latest', 'search']:
        if Choice != None:
            print('You entered an incorrect value.')
        Choice = input('Enter choice: ')

    if Choice == 'category':
        category()
    elif Choice == 'latest':
        latest()
    elif Choice == 'search':
        search()

    pgid = int(input('How many pages do you want to download: '))
    totalImageToDownload = str(24 * pgid)
    print('Number of Wallpapers to Download: ' + totalImageToDownload)
    for j in range(1, pgid + 1):
        downloadPage(j, totalImageToDownload)

if __name__ == '__main__':
    main()
