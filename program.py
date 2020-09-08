from youtube_search import YoutubeSearch
import youtube_dl

def grab_video_link(search_query): #gets youtube link from search input 
    results = YoutubeSearch(search_query, max_results=1).to_dict()
    return 'https://www.youtube.com/watch?v={}'.format(results[0]['id'])

def queries_from_search(search_query):
	queries = search_query.split(",")
	return queries 

def onFinish(dl):
    if dl['status'] == 'finished':
        print('Done downloading, converting right now...')

def dl_link(link,auto):
	if "list" in link:
	        ending = "Would you like to download this playlist? Y/n "
	        no_playlist = False
	else:
	    ending = "Would you like to download this video? Y/n " 
	    no_playlist = True
	ydl_opts = {
	    'format':'bestaudio/best',
	    'outtmpl':'Tydowned/%(title)s.%(ext)s',
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

def loopDL(search_queries,enable_auto):
    num_queued = len(search_queries)
    plural = 's' if len(search_queries) > 1 else ''
    print("{} thing{} to download".format(num_queued ,plural))

    completed = 0
    for search in search_queries:
        video_link = grab_video_link(search)
        if dl_link(video_link,enable_auto):
            completed += 1
            print('\033[92m' + 'Downloaded %d / %d\033[0m' % (completed,num_queued))
        else:
            completed+=0
            num_queued -= 1
            print("\033[91mRemoved: '{}'\033[0m".format(search))

def main():
    search = input("Video: ")
    search_queries = queries_from_search(search)
    loopDL(search_queries,1)

if __name__ == '__main__':
    main()
