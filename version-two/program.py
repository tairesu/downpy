from ast import parse
from operator import truediv
from pyparsing import Or
from os import path
from youtube_search import YoutubeSearch
import youtube_dl
import argparse
import subprocess

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

	if dataPoints['auto_download'] or input(ending).lower() == "y":
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])
		return True
	
	return False
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
	print(args.current)
	if args.songs:
		dataPoints['search_terms'] = args.songs
	
	if args.auto:
		print("Auto download enabled")
		dataPoints['auto_download'] = True

	if args.destination and path.isdir(args.destination):
		dataPoints['target_destination'] = args.destination

	if args.current:
		currentsong = subprocess.run(['playerctl','metadata','title'], stdout=subprocess.PIPE).stdout.decode('utf-8')
		dataPoints['search_terms'].append(currentsong[0:-1]) #Removes the \n from the decoded result

	return args
	##parse args, run conditions, cleanup
	
def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("songs", nargs='*', default=None, help="Add as many songs as you want by seperating them into their own double quotes")
	parser.add_argument("-a","--auto", help="Download songs without being asked to confirm the downloads", action="store_true")
	parser.add_argument("-d","--destination", help="Sets the destination of your downloads")
	parser.add_argument("-c", "--current", help="Downloads whatever song is being played", action="store_true")
	
	args = parser.parse_args()	
	return args

	

def main():
	args = init_args()
	if not (args.songs or args.current):
		search = input("Video: ")
		dataPoints['search_terms'] = queries_from_search(search)
	print(dataPoints['search_terms'])
	loopDL(dataPoints['search_terms'])


if __name__ == '__main__':
    main()
