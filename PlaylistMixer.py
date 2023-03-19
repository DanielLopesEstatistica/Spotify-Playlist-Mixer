import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from tkinter import *
import random 

client_id = 'YourClientID'
client_secret = 'YourClientSecret'
redirect_uri = 'http://localhost:8000/callback'
scope = 'playlist-read-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

playlists = sp.current_user_playlists()

names_playlists = []

for n in range(len(playlists['items'])):
    names_playlists.append(playlists['items'][n]['name'])

# create the main window
root = Tk()

# create a list to store the selected strings
choosen_playlists = []

# create a function to update the selected strings list
def update_selected_playlists():
    choosen_playlists.clear()
    for index, name in enumerate(names_playlists):
        if checkbuttons_vars[index].get():
            choosen_playlists.append(name)

# create a list of variables to store the state of each checkbutton
checkbuttons_vars = []
for name in names_playlists:
    var = IntVar()
    checkbuttons_vars.append(var)

# create a checkbutton for each string in the list
max_rows = 10
for index, name in enumerate(names_playlists):
    row = index % max_rows
    column = index // max_rows
    checkbutton = Checkbutton(root, text=name, variable=checkbuttons_vars[index], command=update_selected_playlists)
    checkbutton.grid(row=row, column=column, sticky=W)
    
# create a button to close the window
close_button = Button(root, text="Mix!", command=root.destroy)
close_button.grid(row=max_rows, column=0, sticky=W)
    
# run the main loop
root.mainloop()

songs_ids = []

for names in choosen_playlists:
    playlists = sp.current_user_playlists()
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == names:
            playlist_id = playlist['id']
            break

    if playlist_id is None:
        print("Playlist not found")
    else:
        # Get the tracks in the playlist
        tracks = sp.playlist_items(playlist_id)
        for track in tracks['items']:
            songs_ids.append(track['track']['id'])

scope = 'playlist-modify-public'

# Create a SpotifyOAuth object with the client ID, client secret, redirect URI, and scope
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

# Create a Spotify object with the authentication manager
sp = spotipy.Spotify(auth_manager=auth_manager)

# Create a new playlist with the name "My New Playlist"
playlist = sp.user_playlist_create(user=sp.current_user()['id'], name='Seu Mix Temporário')

songs_ids = list(set(songs_ids))

random.shuffle(songs_ids)

track_ids = songs_ids

for iterations in range(int(len(songs_ids)/100) + 1):
    tracks_to_add = track_ids[:min(100, len(track_ids))]
    track_ids = track_ids[min(100, len(track_ids)):]
    sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlist['id'], tracks=tracks_to_add)
