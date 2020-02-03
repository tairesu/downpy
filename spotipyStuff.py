import spotipy
import sys
import spotipy.util as util
import urlStuff

output = []
class User:
    def __init__(self,spotify_obj):
        self.spotify_obj = spotify_obj
        self.id = self.getUserId()
        self.playlists = self.getPlaylists()
        self.savedTracks = self.getSavedTracks()

    def getUserId(self): #getUserInfo grabs playlists,saved tracks
        return self.spotify_obj.current_user()['id']

    def getSavedTracks(self):
        tracks = self.spotify_obj.current_user_saved_tracks(limit=50)['items']
        return ["{1} {0}".format(track['track']['name'],track['track']['artists'][0]['name']) for track in tracks ]
    def getPlaylists(self):
        playlists = self.spotify_obj.current_user_playlists() 
        return { playlist['name']:playlist['id'] 
                for playlist in playlists['items'] if playlist['owner']['id'] == self.id }
    def showTracks(self):
        print(self.savedTracks)
    def showPlaylists(self):
        for count, playlist in enumerate(self.playlists):
                print('[%d] %s' % (count,playlist))
class Artist:
    def __init__(self,spotify_obj,name):
        self.name = name
        self.spotify_obj = spotify_obj
        self.id = self.getArtist()
        self.topTen = self.getTopTen()
        self.albums = self.getAlbums()
    def getArtist(self):
        artist = self.spotify_obj.search(q=self.name,limit=1,type='artist')
        return artist['artists']['items'][0]['id']
        
    def getTopTen(self):
        top_songs = self.spotify_obj.artist_top_tracks(self.id,country='US')
        #i would prefer just the names for now
        return ["{1} {0}".format( song['name'],self.name) for song in top_songs['tracks'] ]
    
    def getAlbums(self):
        albums = self.spotify_obj.artist_albums(self.id,album_type='album',country='US',limit='30')
        return { album['name']:album['id'] for album in albums['items'] }

    def showTopTen(self):
        print(self.topTen)

    def showAlbums(self):
        for count, album_name in enumerate(self.albums.keys()):
            print('[%d] : %s' % ( count,album_name))
class Playlist:
    def __init__(self,spotify_obj,playlistID,userID):
        self.id = playlistID
        self.spotify_obj = spotify_obj
        self.user = userID
        self.tracks = self.tracksInPlaylist()

    def tracksInPlaylist(self):
        playlist_tracks = self.spotify_obj.user_playlist(self.user,self.id,fields="tracks")
        return ["{1} {0}".format(item['track']['name'],item['track']['artists'][0]['name']) for item in playlist_tracks['tracks']['items']]

    def showTracks(self):
        print("\n")
        for track in self.tracks:
            print("{}".format(track))
    
class Album:
    def __init__(self,spotify_obj,albumID):
        self.id = albumID
        self.spotify_obj = spotify_obj
        self.tracks = self.getAlbumTracks()
        self.name = self.getAlbumName()

    def getAlbumTracks(self):
        album_tracks = self.spotify_obj.album_tracks(self.id,limit=30)
        return ["{1} {0}".format(album['name'],album['artists'][0]['name']) for album in album_tracks['items']]
    
    def getAlbumName(self):
    	#album = self.spotify_obj.albums(self.id)
    	
    	self.name = self.id

    def showTracks(self):
    	
    	for track in self.tracks:
    		print("{}".format(track))
        

    def showName(self):
    	print(self.name)

def initialize():
    def setUser():
        if len(sys.argv) > 1:
            username = sys.argv[1] # argv[0] is python, argv[1] is after .py file 
            return username
        else:
            print("Usage: %s username" %(sys.argv[0]))
            sys.exit()
    def ini_spotify(user):
        scope = 'user-library-read'
        token = util.prompt_for_user_token(user,scope,client_id='5ad7665f08b14b29ab781dfc52af4a41',client_secret='33e91a857dee42c9b3dda13b26e55104',redirect_uri='http://localhost/')
        if token ==None:
            print("Cant get token for", user)  
            sys.exit()

        return token
    username = setUser()
    token = ini_spotify(username)
    return token


"""
Lets take it a step further:
    On execution of app choose what to return 
    [0] Artist Top 10
    [1] My playlists & tracks
    [2] Artists Albums & tracks
    [3] My saved tracks

    in the future: give iniProgram the getUserInfo obj so the other programs dont have to
"""
def runSpotipyProgram(spotify_obj):
    file1 = open("program.txt","r")
    text = file1.read()
    print(text)
    
    def handle_topten():
        artist_name = input("Choose Artist: ")
        artistObj = Artist(spotify_obj,artist_name)
        artistObj.showTopTen()
        return artistObj.topTen
        

    def handle_albums():
        #1) print albums in number form 2) select album from number 
        artist_name = input("Choose Artist: ")
        artistObj = Artist(spotify_obj,artist_name)
        artistObj.showAlbums()        
        album_selection = input("Enter album number:  ")
        albumID = list(artistObj.albums.values())[int(album_selection)]
        albumName = list(artistObj.albums.keys())[int(album_selection)]
        albumObj = Album(spotify_obj,albumID)
        print('\nSongs in Album:',albumName)
        albumObj.showTracks()
        return albumObj.tracks

    def handle_playlists():
        userObj = User(spotify_obj)
        userObj.showPlaylists()
        playlist_choose = input("Enter playlist number: ")
        playlistID = list(userObj.playlists.values())[int(playlist_choose)]
        playlistName = list(userObj.playlists.keys())[int(playlist_choose)]
        playlistObj = Playlist(spotify_obj,playlistID,userObj.id)
        print('\nSongs in Playlist:',playlistName)
        playlistObj.showTracks()
        return playlistObj.tracks

    def handle_saved():
        userObj = User(spotify_obj)
        userObj.showTracks()
        return userObj.savedTracks
        
    appFeature = input("What to download? ")
    featureDict = {
        '0': handle_topten,
        '1': handle_albums,
        '2': handle_playlists,
        '3': handle_saved
        }
    if appFeature in featureDict:
        output = featureDict[appFeature]()
        download = input("Is this what you want to download? Y/n ")
        if download.lower() == "y":
            run_auto = input("Automatically download? Y/n ")
            if run_auto.lower() == "y":
                urlStuff.loopDL(output,1)
            else:
                urlStuff.loopDL(output,0)
        
    else:
        print('Not an option my nigga')

def initProgram(spotify_obj):
    print(
	"[0] Basic Youtube Search\n[1] Spotify Scraper\n")
    def handleBasic():
        yt_search = input("Video Search: ")
        queries = yt_search.split(",")
        download = input("Is this what you want to download? Y/n ")
        if download.lower() == "y":
            run_auto = input("Automatically download? Y/n ")
            if run_auto.lower() == "y":
                urlStuff.loopDL(queries,1)
            else:
                urlStuff.loopDL(queries,0)
    def handleSpotify():
        #run imported spotify code
        runSpotipyProgram(spotify_obj)

    option = input("Enter Number: ")
    options = {
        '0':handleBasic,
        '1':handleSpotify
            }
    if option in options:
        options[option]()
    else:
        print("Can't do that")


def main():
    token = initialize()
    sp = spotipy.Spotify(auth=token)
    initProgram(sp)
    #iniProgram(sp)
    
if __name__ == '__main__':
    main()

