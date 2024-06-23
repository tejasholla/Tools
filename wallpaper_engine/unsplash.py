import os
import requests
import urllib.parse
import json

# Determine the path to the Pictures directory and create the Wallpapers folder if it doesn't exist
pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
wallpapers_dir = os.path.join(pictures_dir, "Wallpapers")
os.makedirs(wallpapers_dir, exist_ok=True)

BASEURL = "https://api.unsplash.com/"
headers = dict()

global APIKEY
APIKEY = ""

def set_headers():
    global headers
    headers = {
        "Authorization": f"Client-ID {APIKEY}"
    }

def category():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    nature  - For 'Nature' wallpapers only.
    technology - For 'Technology' wallpapers only.
    people  - For 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ').lower()
    ctags = {'all': 'all', 'nature': 'nature', 'technology': 'technology', 'people': 'people'}
    ctag = ctags[ccode]

    BASEURL = f'https://api.unsplash.com/search/photos?query={ctag}&client_id={APIKEY}&page='

def latest():
    global BASEURL
    print('Downloading latest')
    BASEURL = f'https://api.unsplash.com/photos?client_id={APIKEY}&order_by=latest&page='

def search():
    global BASEURL
    query = input('Enter search query: ')
    BASEURL = f'https://api.unsplash.com/search/photos?query={urllib.parse.quote_plus(query)}&client_id={APIKEY}&page='

def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    urlreq = requests.get(url, headers=headers)
    pagesImages = urlreq.json()

    # For search results
    if 'results' in pagesImages:
        pageData = pagesImages["results"]
    else:  # For latest photos
        pageData = pagesImages

    for i in range(len(pageData)):
        currentImage = (((pageId - 1) * 10) + (i + 1))  # Unsplash returns 10 images per page

        url = pageData[i]["urls"]["full"]

        filename = os.path.basename(urllib.parse.urlparse(url).path) + '.jpg'
        osPath = os.path.join(wallpapers_dir, filename)
        if not os.path.exists(osPath):
            imgreq = requests.get(url, headers=headers)
            if imgreq.status_code == 200:
                print(f"Downloading : {filename} - {currentImage} / {totalImage}")
                with open(osPath, 'wb') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
            else:
                print(f"Unable to download {filename} - {currentImage} / {totalImage}")
        else:
            print(f"{filename} already exists - {currentImage} / {totalImage}")

def main():
    set_headers()

    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "search" for downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['category', 'latest', 'search']:
        if Choice is not None:
            print('You entered an incorrect value.')
        Choice = input('Enter choice: ')

    if Choice == 'category':
        category()
    elif Choice == 'latest':
        latest()
    elif Choice == 'search':
        search()

    pgid = int(input('How many pages do you want to download: '))
    totalImageToDownload = str(10 * pgid)  # Unsplash returns 10 images per page
    print(f'Number of Wallpapers to Download: {totalImageToDownload}')
    for j in range(1, pgid + 1):
        downloadPage(j, totalImageToDownload)

if __name__ == '__main__':
    main()
