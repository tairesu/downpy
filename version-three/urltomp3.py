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

def initiate_search(search):
	searchTerms = search.split(delimeter)
	for i,term in enumerate(searchTerms):
		search = SearchTerm(term)

def set_destination(path=music_folder_path):
	global destination
	destination = path

def display(results):
		print(f"***********************************************")
		for i,video in enumerate(results):
			print(f"[{i}]\n")
			for attr in video.keys():
				if attr not in ['shelfTitle','thumbnails','descriptionSnippet','richThumbnail','accessibility','id']:
					print(f"		{attr.capitalize()}: {video[attr]}")

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
		print(self.results)
		self.specified_result = self.filtered_result()
		self.url = self.get_url()
		self.noplaylist = self.is_playlist()
		self.dl_url()

	def get_results(self):
		#self.results = YoutubeSearch(self.term, max_results).to_dict() 
		return Search(self.term, limit=max_results).result()['result']
	
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
			else:
				i = i + 1
		assert selection != {}
		return selection
	
	def get_url(self):
		return self.specified_result['link']

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
		return True
		
	def show_url(self):
		print(self.url)

def main():
	try:
		initiate_search(input("What can I get for you?: "))
	except EOFError or KeyboardInterrupt:
		print("\nSee ya later!") 

if __name__ == '__main__':
	main()
