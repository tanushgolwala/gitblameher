from hmac import new
import os
from youtubesearchpython import *
from pytubefix import YouTube

def get_song_url(song_name):
    try:
        videosSearch = VideosSearch(song_name, limit = 1)
        url = videosSearch.result()['result'][0]['link']
        print(url)
        return url
    except Exception as e:
        print(f"Error in get_song_url: {e}")
        return None
    
def download_song(song_url, song_name):
    yt = YouTube(song_url, use_oauth=True, allow_oauth_cache=True)
    print(yt.title)
    
    ys = yt.streams.get_audio_only()
    ys.download(mp3=True, output_path='mv_songs', filename=song_name)
    
def get_url_and_download_song(song_name, artist):
    song_url = get_song_url(song_name + artist + ' song lyric video')
    if song_url:
        download_song(song_url, song_name)
        return True
    return False

# print(get_url_and_download_song('Paradise'))