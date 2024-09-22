import requests
from bs4 import BeautifulSoup
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "d3efa15c066d4e8db34b30b95dbc5674"
CLIENT_SECRET = "23a1bce59b0843488311d659bf4ad392"
redirect_url = "http://example.com"
timemachine = input("Wich year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
top100class = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"

url = f"https://www.billboard.com/charts/hot-100/{timemachine}/"
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               redirect_uri=redirect_url,
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username="Joshua Hermoso"))

user_id = sp.current_user()["id"]
response = requests.get(url)
website = response.text

soup = BeautifulSoup(website, "html.parser")

get_songs = soup.select("li ul li h3")
get_all_songs = [songs.getText().strip() for songs in get_songs]
musics = get_all_songs
track_uri = []
year = timemachine.split("-")[0]
for idx in musics:
    results = sp.search(q=idx, type="track",)
    try:
        track = results['tracks']['items'][0]['uri']
        track_uri.append(track)
    except IndexError:
        print(f"{idx}doesn't exist in Spotify. Skipped")

user_id = sp.me()['id']

playlist_name = f"{timemachine} Billboard 100"
playlist_description = "playlist that will take you back in time"
new_playlist = sp.user_playlist_create(user=user_id,
                                       name=playlist_name,
                                       public=False,
                                       description=playlist_description)

sp.playlist_add_items(playlist_id=new_playlist['id'], items=track_uri)

