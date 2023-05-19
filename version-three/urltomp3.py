from youtube_search import YoutubeSearch
from youtubesearchpython import Search
import yt_dlp
import asyncio
import os
import subprocess

music_folder_path = "/home/tyro/music/"
destination = music_folder_path
delimeter = ";"

def set_destination(path):
	global destination
	destination = path

def file_exists(title):
	modifiedpath = f"{title}*"
	matched_files = subprocess.run(
		['find',music_folder_path,'-iname',modifiedpath],
		stdout=subprocess.PIPE).stdout.decode('utf-8')
	return (matched_files != "", matched_files)

def is_validURL(url):
	if isinstance(url, str):
		assert "www.youtube.com/" in url
		return True
	return False

class SearchTerm():
	def __init__(self, term, max_results=3):
		self.term = term
		self.max_results = max_results
		self.results = self.get_results()
		self.specified_result = self.filtered_result()
		self.url = self.get_url()
		self.noplaylist = self.is_playlist()
		self.dl_url()
		#print(file_exists(self.specified_result['title']))

	def get_results(self):
		#self.results = YoutubeSearch(self.term, self.max_results).to_dict() 
		self.results = Search(self.term, limit=self.max_results).result()['result']
		return self.results

	def filtered_result(self):
		self.display(self.results)
		index = input("Which of these do you want? [0-2]")
		if type(int(index)) == int: 
			assert int(index) < len(self.results)
			return self.results[int(index)]
		return False
	
	def display(self,arr):
		for i,video in enumerate(arr):
			print(f"[{i}]\n")
			for attr in video.keys():
				if attr not in ['shelfTitle','thumbnails','descriptionSnippet','richThumbnail','accessibility','id']:
					print(f"		{attr.capitalize()}: {video[attr]}")
	
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

		print(f"This is the destination i am downloading to: {destination}")
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
		print(file_exists(self.specified_result['title']))
		if file_exists(self.specified_result['title'])[0]:
			print('You already have this song!')
			return False
		
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download(self.url)
		return True
		
	def show_url(self):
		print(self.url)

def initiate_search(search):
	searchTerms = search.split(delimeter)
	for i,term in enumerate(searchTerms):
		search = SearchTerm(term)

def main():
	try:
		initiate_search(input("What can I get for you?: "))
	except EOFError or KeyboardInterrupt:
		print("\nSee ya later!") 

if __name__ == '__main__':
	main()
