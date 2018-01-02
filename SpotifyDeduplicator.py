import sys

import spotipy
import spotipy.util as util


CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT = ''
USERNAME = ''
SCOPE = 'playlist-modify-private playlist-read-private playlist-read-collaborative'

clear = "\n" * 100

if len(sys.argv) >3:
    CLIENT_ID = sys.argv[1]
    CLIENT_SECRET = sys.argv[2]
    REDIRECT = sys.argv[3]
else:
    print("Usage: %s client_id client_secret redirect_url" % (sys.argv[0]))
    sys.exit()

token = util.prompt_for_user_token(USERNAME, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    #Get User's playlists
    results = sp.current_user_playlists(limit=50)
    play_count = len(results['items'])
    play_num = -1

    print(clear)
    for i, item in enumerate(results['items']):
        print("%d %s" %(i, item['name']))
    print('\n\n')

    while(play_num == -1):
        try:
            play_num = int(input("Enter the number of the playlist to deduplicate: "))
            if (play_num < 0 or play_num >= play_count): #if the chosen number is out of the range of playlists...
                print('Invalid Playlist Number\n')
                play_num = -1 #...we set play_num to -1 so it will have to check again
        except ValueError:
            print('Invalid Input!\n')

    playlist = results['items'][play_num]['id'] #get ID of chosen playlist

    #Start Deduplication of Playlist
    results = sp.user_playlist(sp.current_user()['id'],playlist)
    song_list = []
    dup_list = []

    for i, item in enumerate(results['tracks']['items']):
        if item['track']['id'] in song_list:
            dup_list.append({"uri":item['track']['id'], "positions":[i]})
        song_list.append(item['track']['id'])

    sp.user_playlist_remove_specific_occurrences_of_tracks(sp.current_user()['id'], playlist, dup_list)

    print("Duplicate Songs removed from Playlist!")

else:
    print("Could not get token for user...")


