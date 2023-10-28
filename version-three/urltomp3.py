from youtube_search import YoutubeSearch
from youtubesearchpython import Search
import yt_dlp
import asyncio
import os
import subprocess

music_folder_path = "/home/tyro/music/"
destination = music_folder_path
delimeter = ";"
per_page = 3
max_results = 21
keep_open = True

#Creates objects from each search term in main() input
def initiate_search(search):
	searchTerms = search.split(delimeter)
	for i,term in enumerate(searchTerms):
		search = SearchTerm(term)

def set_destination(path=music_folder_path):
	global destination
	destination = path

# Displays the metadata how we want it to

def display(results):
	for i,video in enumerate(results):
		if video['type'] == "playlist":
			condition = "Has " + video['videoCount'] + " video(s)"
		elif video['type'] == "video":
			condition = video['accessibility']['duration'] + " long\n\t" +  video['viewCount']['short']

		print(f"""
[{i}]
	{video['type']}: {video['title']}
	{condition}
	{video['link']}
	uploaded by '{video['channel']['name']}'
				""")
		

		

def song_exists(title):
	modifiedpath = f"{title}*"
	matched_files = subprocess.run(
		['find',music_folder_path,'-iname',modifiedpath],
		stdout=subprocess.PIPE).stdout.decode('utf-8')
	print(matched_files)
	return (matched_files != "", matched_files)

def is_validURL(url):
	if isinstance(url, str):
		assert "www.youtube.com/" in url
		return True
	return False

class SearchTerm():
	def __init__(self, term):
		self.term = term
		self.results = self.get_results()
		self.specified_result = self.filtered_result()
		self.url = self.specified_result['link']
		self.noplaylist = self.is_playlist()
		self.dl_url()

	def get_results(self):
		#self.results = YoutubeSearch(self.term, max_results).to_dict() 
		return Search(self.term, limit=max_results).result()['result']
	
	#Paginates results and handles video selection
	def filtered_result(self):

		selection = {}
		i = 0
		while i <= (max_results // per_page) and selection == {}:
			start, finish = i * per_page, (i * per_page) + per_page
			section = self.results[start:finish]
			display(section)
			index = input(f"Which one do you want (0-{len(section) - 1})?")
			if index.isdigit():
				assert int(index) < len(section)
				selection = section[int(index)]
			elif index.lower() in ["reset","-r","quit"]:
				main()
			else:
				i = i + 1
		assert selection != {}
		return selection

	def is_playlist(self):
		if self.specified_result['type'] == "playlist":
			return False
		return True
	 
	def on_finish(self,dl):
		if(dl['status'] == 'finished'):
			print('/nDownload Finished Converting to mp3')
	
	def dl_url(self):
		if(self.specified_result['type']=="playlist"):
			set_destination(music_folder_path + self.specified_result['title'] + '/')

		ydl_opts = {
		'xyz': '%(playlist)s',
	    'format':'bestaudio/best',
	    'outtmpl':'{}%(title)s.%(ext)s'.format(destination),
	    'noplaylist': '{}'.format(self.noplaylist),
	    'quiet':False,
	    'progress_hooks': [self.on_finish],
	    'postprocessors':[{
	        'key':'FFmpegExtractAudio',
	        'preferredcodec':'mp3',
	        'preferredquality':'192',
	        }]
	    }
		if (song_exists(self.specified_result['title'])[0]):
			print('You already have this song!')
			return False

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download(self.url)

		if keep_open == True:
			main("\nWhat else can I get you?") 
		return True
		
	def show_url(self):
		print(self.url)

def main(opening="What can I get for you?: "):
	try:
		initiate_search(input(opening))
	except EOFError or KeyboardInterrupt:
		print("\nSee ya later!") 

if __name__ == '__main__':
	main()
