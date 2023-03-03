
from ast import parse
from operator import truediv
from pyparsing import Or
from os import path
from youtube_search import YoutubeSearch
import yt_dlp
import argparse
import subprocess


class YTLogger(object):
	def error(self,msg):
		print(msg)

	def warning(self, msg):
		pass

	def debug(self, msg):
		pass

system_variables = {
    'search_terms': [],
    'no_playlist': True,
    'auto_download' : False,
    'results' : [],
    'delimiter' : ";",
    'target_destination': '/home/tyro/music/',
	'ending': ''
}

def display_results():

	video_data = system_variables['results'][0]

	expression = f"""

	Title: {video_data['title']}
	Duration: {video_data['duration']}
	URL: http://www.youtube.com/watch?v={video_data['url_suffix']}
	Channel: {video_data['channel']} 
	Views: {video_data['views']}
	Published: {video_data['publish_time']}

	"""

	print(expression)

#Returns the first Youtube URL from a singular search 
def get_video_url(search_term):  
    video_data = YoutubeSearch(search_term, max_results=1).to_dict()
    system_variables['results'] = video_data
    return 'https://www.youtube.com/watch?v={}'.format(video_data[0]['id'])

def queries_from_search(search_query):
	queries = search_query.split(system_variables['delimiter'])
	return queries 

def onFinish(dl):
    if dl['status'] == 'finished':
        print('Done downloading, converting right now...')

#Determines if the watch link is a playlist; sets program response accordingly
def no_playlist(link):

	if "list" in link:
		ending = "Would you like to download this playlist? Y/n "
		no_playlist = False
	else:
		ending = "Would you like to download this song? Y/n "
		no_playlist = True

	system_variables['no_playlist'] = no_playlist 
	system_variables['ending'] = ending
	return no_playlist
# Instead of parameters, why not just pass a single object? 
# Here I need the youtube link, no_playlist, 
def dl_link(link):
	noplaylist = no_playlist(link)
	
	ydl_opts = {
	    'format':'bestaudio/best',
	    'outtmpl':'{}%(title)s.%(ext)s'.format(system_variables['target_destination']),
	    'noplaylist': noplaylist,
	    'quiet':False,
	    'progress_hooks': [onFinish],
	    'postprocessors':[{
	        'key':'FFmpegExtractAudio',
	        'preferredcodec':'mp3',
	        'preferredquality':'192',
	        }]
	    }

	if system_variables['auto_download'] or input(system_variables['ending']).lower() == "y":
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])
		return True
	
	return False
def loopDL(search_terms):
    num_queued = len(search_terms)
    plural = 's' if len(search_terms) > 1 else ''
    print("{} thing{} to download".format(num_queued ,plural))

    completed = 0
    for term in search_terms:
        video_url = get_video_url(term)
        display_results()

        # Commences the download
        if dl_link(video_url):
            completed += 1
            print('\033[92m' + 'Downloaded %d / %d\033[0m' % (completed,num_queued))
        else:
            completed+=0
            num_queued -= 1
            print("\033[91mRemoved: '{}'\033[0m".format(term))

def init_args():
	args = get_args()
	print(args.current)
	if args.songs:
		system_variables['search_terms'] = args.songs
	
	if args.auto:
		print("Auto download enabled")
		system_variables['auto_download'] = True

	if args.destination and path.isdir(args.destination):
		system_variables['target_destination'] = args.destination

	if args.current:
		currentsong = subprocess.run(['playerctl','metadata','title'], stdout=subprocess.PIPE).stdout.decode('utf-8')

		#Removes the \n from the decoded result
		system_variables['search_terms'].append(currentsong[0:-1]) 

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
		system_variables['search_terms'] = queries_from_search(search)
	loopDL(system_variables['search_terms'])


if __name__ == '__main__':
    main()
