import requests
import bs4
import argparse

# reads search query
parser = argparse.ArgumentParser(description="Downloads albums from bandcamp")
parser.add_argument("search", metavar="SEARCH", type=str, help="Album name")
parser.add_argument('-a', '--all_pages', action='store_true', help="Checks other pages if true")
args = parser.parse_args()
search_string = args.search
all_pages = args.all_pages

# bandcamp search link
bandcamp_search_link = 'https://bandcamp.com/search'
# request for the page
album_res = requests.get(bandcamp_search_link + "?q=" + search_string)
# checks if no errors ocurred
album_res.raise_for_status()

def print_items(items):
    '''prints the results'''
    for item in items:
        item_type = item.select_one('div.itemtype').getText().strip('\n ')
        if item_type.lower() == "album":
            heading = item.select_one('div.heading > a').getText().strip('\n ')
            subhead = item.select_one('div.subhead').getText().strip('\n ')
            length = item.select_one('div.length').getText().strip('\n ')
            release_date = item.select_one('div.released').getText().strip('\n ')
            link = item.select_one('div.itemurl > a').getText().strip('\n ')
    
            print('----------------------------------------------------')
            print(heading)
            print(subhead)
            print(length)
            print(release_date)
            print(link)

# html parsing
soup = bs4.BeautifulSoup(album_res.text, "html.parser")
items = soup.select('#pgBd > div.search > div.leftcol > div > ul > li > div')

# search pages
pages = [item.get('href') for item in soup.select('#pgBd > div.search > div.leftcol > div > div > div > ul > li > a')]

# prints the items for the first page
print_items(items)

if all_pages:
    # checks the other pages
    for page in pages:
        # request for the page
        album_res = requests.get(bandcamp_search_link + page)
        # checks if no errors ocurred
        album_res.raise_for_status()
        # html parsing
        soup = bs4.BeautifulSoup(album_res.text, "html.parser")
        items = soup.select('#pgBd > div.search > div.leftcol > div > ul > li > div')
        # prints_items
        print_items(items)