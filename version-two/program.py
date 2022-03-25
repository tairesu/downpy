from ast import parse
from operator import truediv
from youtube_search import YoutubeSearch
import youtube_dl
import argparse

dataPoints = {
    'search_terms': [],
    'is_playlist': False,
    'auto_download' : False,
    'results' : [],
	'delimiter' : ";",
	'target_destination': '/home/tyro/Music/'

}

def grab_video_link(search_query): #gets youtube link from search input 
    results = YoutubeSearch(search_query, max_results=1).to_dict()
    return 'https://www.youtube.com/watch?v={}'.format(results[0]['id'])

def queries_from_search(search_query):
	queries = search_query.split(dataPoints['delimiter'])
	return queries 

def onFinish(dl):
    if dl['status'] == 'finished':
        print('Done downloading, converting right now...')


# Instead of parameters, why not just pass a single object? 
# Here I need the youtube link, no_playlist, 
def dl_link(link):
	print(dataPoints)
	if "list" in link:
	        ending = "Would you like to download this playlist? Y/n "
	        no_playlist = False
	else:
	    ending = "Would you like to download this video? Y/n " 
	    no_playlist = True
	ydl_opts = {
	    'format':'bestaudio/best',
	    'outtmpl':'{}%(title)s.%(ext)s'.format(dataPoints['target_destination']),
	    'noplaylist': dataPoints['is_playlist'],
	    'progress_hooks': [onFinish],
	    'postprocessors':[{
	        'key':'FFmpegExtractAudio',
	        'preferredcodec':'mp3',
	        'preferredquality':'192',
	        }]
	    }

	if not dataPoints['auto_download']:
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

def loopDL(search_queries):
    num_queued = len(search_queries)
    plural = 's' if len(search_queries) > 1 else ''
    print("{} thing{} to download".format(num_queued ,plural))

    completed = 0
    for search in search_queries:
        video_link = grab_video_link(search)
        if dl_link(video_link):
            completed += 1
            print('\033[92m' + 'Downloaded %d / %d\033[0m' % (completed,num_queued))
        else:
            completed+=0
            num_queued -= 1
            print("\033[91mRemoved: '{}'\033[0m".format(search))

def init_args():
	args = get_args()
	if args.songs:
		dataPoints['search_terms'] = args.songs
	
	if args.auto:
		print("Auto download enabled")
		dataPoints['auto_download'] = True

	return args
	##parse args, run conditions, cleanup
	
def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("songs", nargs='*', default=None)
	parser.add_argument("-a","--auto", action="store_true")
	
	args = parser.parse_args()

	
		
	return args

	

def main():
	args = init_args()
	if not args.songs:
		search = input("Video: ")
		dataPoints['search_terms'] = queries_from_search(search)
	print(dataPoints['search_terms'])
	loopDL(dataPoints['search_terms'])


if __name__ == '__main__':
    main()
