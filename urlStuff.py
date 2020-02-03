from bs4 import BeautifulSoup
import urllib.request
import youtube_dl
"""
reapLink('j dilla track 31') => https://www.youtube.com/watch?v=whateverVideois 
"""

def reapLink(search): #gets youtube version of search input 
    splitSearch = search.lower().split(" ")
    searchQuery = 'http://youtube.com/results?search_query='
    if len(splitSearch) > 1:
        #we need to replace spaces with plusses
        for word in splitSearch:
            searchQuery += word + '+'
        searchQuery = searchQuery[:-1]
    elif len(splitSearch) == 1:
        #if string has no spaces
        searchQuery += splitSearch[0]
    else:
        print("Put something nigga")

    #print(searchQuery)
    with urllib.request.urlopen(searchQuery) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    result = soup.select('h3 >a')[0]
    videoTime = result.parent.span.string 
    #print(videoTime) returns " - Duration: ..." 
    full_link = 'https://www.youtube.com' + result['href']

    print('\033[94mTitle: %s\033[0m \nLink: %s'% (result['title'],full_link))
    if "Duration" in videoTime:
        #index of ":" is 11 so I use 13 to skip over color and extra space
        print('Duration: %s' % videoTime[13:-1]) 

    return full_link

def onFinish(dl):
    if dl['status'] == 'finished':
        print('Done downloading, converting right now...')

#dl_link(link) takes youtube link and downloads it 
def dl_link(link,auto):
	if "list" in link:
	        ending = "Would you like to download this playlist? Y/n "
	        no_playlist = False
	else:
	    ending = "Would you like to download this video? Y/n " 
	    no_playlist = True
	ydl_opts = {
	    'format':'bestaudio/best',
	    'outtmpl':'Music/%(title)s.%(ext)s',
	    'noplaylist': no_playlist,
	    'progress_hooks': [onFinish],
	    'postprocessors':[{
	        'key':'FFmpegExtractAudio',
	        'preferredcodec':'mp3',
	        'preferredquality':'192',
	        }]
	    }

	if auto == 0:
	    response = input(ending)
	    if response.lower() == "y": #go on with download
	        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	            ydl.download([link])
	        return True

	    else:
	        return False
	else:
	    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	            ydl.download([link])
	    return True
"""
   queries is list
   loopDL goes through list and for every query in the array, it gets a youtube watch link from reapLink 
"""

def loopDL(queries,enable_auto):
    queued = len(queries)
    print("%d thing(s) to download" % queued)
    completed = 0
    for query in queries:
        link_str = reapLink(query)
        

        if dl_link(link_str,enable_auto):
            completed += 1
            print('\033[92m' + 'Downloaded %d / %d\033[0m' % (completed,queued))
        else:
            completed+=0
            print("\033[91mRemoved: '%s'\033[0m" % query )
"""
def initProgram():
    print(
    "[0] Basic Youtube Search\n",
    "[1] Spotify Scraper\n",
            )
    def handleBasic():
        yt_search = input("Video Search: ")
        queries = yt_search.split(",")
        loopDL(queries)
    def handleSpotify():
        #run imported spotify code
        print('coming soon')

    option = input("Enter Number: ")
    options = {
        '0':handleBasic,
        '1':handleSpotify
            }
    if option in options:
        options[option]()
    else:
        print("Can't do that")
"""
def main():
    initProgram()
if __name__ == '__main__':
    #if python is executed on this file __name__ = main 
    #if another file imports this file, __name__ != main
    main()
