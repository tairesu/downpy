from youtube_search import YoutubeSearch
from youtubesearchpython import Search
import yt_dlp
import asyncio

destination = "/home/tyro/music/"
delimeter = ";"
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
		self.url = self.set_url(self.specified_result)
		self.noplaylist = self.is_playlist()
		self.dl_url()

	def get_results(self):
		#self.results = YoutubeSearch(self.term, self.max_results).to_dict() 
		self.results = Search(self.term, limit=self.max_results).result()['result']
		return self.results

	def filtered_result(self):
		self.display(self.results)
		index = input("Which of these do you want? [0-2]")
		if isinstance(index, int):
			assert index < self.max_results
			return self.results[index]
		return False
	
	def display(self,arr):
		for i,video in enumerate(arr):
			print(f"[{i}]\n")
			for attr in video.keys():
				if attr not in ['shelfTitle','thumbnails','descriptionSnippet','richThumbnail','accessibility','id']:
					print(f"		{attr.capitalize()}: {video[attr]}")
	
	def set_url(self,link):
		if is_validURL(link):
			self.url = link
			return link
		return False

	def is_playlist(self):
		if self.specified_result['type'] == "playlist":
			self.set_destination(self.destination + self.specified_result['title'] + '/')
			return not True
		return not False
	 
	def set_destination(self, path):
		self.destination = path

	def on_finish(self,dl):
		if(dl['status'] == 'finished'):
			print('Download Finished Converting to mp3')
	def dl_url(self):
		ydl_opts = {
		'xyz': '%(playlist)s',
	    'format':'bestaudio/best',
	    'outtmpl':'{}%(title)s.%(ext)s'.format(self.destination),
	    'noplaylist': '{}'.format(self.noplaylist),
	    'quiet':False,
	    'progress_hooks': [self.on_finish],
	    'postprocessors':[{
	        'key':'FFmpegExtractAudio',
	        'preferredcodec':'mp3',
	        'preferredquality':'192',
	        }]
	    }
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
