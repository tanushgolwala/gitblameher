from typing import Optional
import lyricsgenius
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")

genius = lyricsgenius.Genius(token)
    
def get_list_of_songs(query):
    songs = genius.search_songs(query)
    return [{'title': song['result']['title'], 'id': song['result']['id']} for song in songs['hits']]

def get_song_lyrics(song_info, artist=Optional[str]):
    if type(song_info) == str:
        if artist:
            song = genius.search_song(song_info, artist)
        else:
            song = genius.search_song(song_info)
    else:
        song = genius.song(song_info)
    
    return song.lyrics

# print(get_song_lyrics('Paradise', 'Coldplay'))
