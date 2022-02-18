#Importing libraries
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from random import randint
from time import sleep
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans

#Defining functions

#Function to get the audio features from a song and saving it on a DF
def SongAudioFeat(song, audio):
    #Creating a DF with the audio Features
    SongAudioFeatures = pd.DataFrame()
    SongAudioFeatures["title"] = [song["tracks"]["items"][0]["name"]]
    SongAudioFeatures["danceability"] = [audio[0]['danceability']]
    SongAudioFeatures["energy"] = [audio[0]['energy']]
    SongAudioFeatures["key"] = [audio[0]['key']]
    SongAudioFeatures["loudness"] = [audio[0]['loudness']]
    SongAudioFeatures["mode"] = [audio[0]['mode']]
    SongAudioFeatures["speechiness"] = [audio[0]['speechiness']]
    SongAudioFeatures["acousticness"] = [audio[0]['acousticness']]
    SongAudioFeatures["instrumentalness"] = [audio[0]['instrumentalness']]
    SongAudioFeatures["liveness"] = [audio[0]['liveness']]
    SongAudioFeatures["valence"] = [audio[0]['valence']]
    SongAudioFeatures["tempo"] = [audio[0]['tempo']]
    
    return(SongAudioFeatures)

#Function to obtain the cluster from a song
def cluster_for_a_Song(SongAudioFeatures, kmeans):
    #Splitting the DF
    y = SongAudioFeatures['title']
    X_audio = SongAudioFeatures.drop(['title'], axis=1)
    #Scaling X
    X_prep = StandardScaler().fit_transform(X_audio)
    #Aplying KMeans to calculate the cluster
    cluster = kmeans.predict(X_prep)
    
    return (cluster)

#End of functions definitions

#Spotipy
secrets_file = open("SpotifySecret.txt","r")
string = secrets_file.read()
secrets_dict={}

for line in string.split('\n'):
    if len(line) > 0:
        secrets_dict[line.split(':')[0]]=line.split(':')[1]

#Initialize SpotiPy with user credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'],
                                                           client_secret=secrets_dict['cs']))

#Code for obtaning the DF from Spotify
'''
def get_playlist_tracks(playlist_id):
    results = sp.user_playlist_tracks("spotify",playlist_id)
    tracks = results['items']
    while results['next']!=None:
        results = sp.next(results)
        tracks = tracks + results['items']
        sleep(randint(1,3))
    return tracks

#Getting the lists
plIds = ["37i9dQZEVXbMDoHDwVN2tF","4NLrcCMFyUgtXor7EjlE7d","5ZyAjPmaz9KOB4f73RFYvi","6MJSGcF4iV79gyo8xZpd8U", 
         "6CfQ2Ptcxju9l6YC2LXzUb", "4hNaqkezNNv7ImufYGHgkf", "1zrx1DCawPLg6Y8AMFgCUZ", "2iBH9S3UXlrtUBxjffgZEh",
         "1cax1gYS1699tnR5bVjtiY", "2P4tjMKY8ORcUU17QBz83q", "5fcPNR6KXA3iYgNrvTDZpY", "62SVVpIhl7b5c82G0IH603"]
         
#Combining all lists in one
all_tracks = []
for i in range(len(plIds)):
    all_tracks = all_tracks + (get_playlist_tracks(plIds[i]))

#Creating the DF
title = []
artist = []
danceability = []
energy = []
key = []
loudness = []
mode = []
speechiness = []
acousticness = []
instrumentalness = []
liveness = []
valence = []
tempo = []


for i in range(len(all_tracks)):
    title.append(all_tracks[i]["track"]["name"])
    artist.append(all_tracks[i]['track']['artists'][0]['name'])
    song_uri = all_tracks[i]["track"]["uri"]
    audio = sp.audio_features(song_uri)
    danceability.append(audio[0]['danceability'])
    energy.append(audio[0]['energy'])
    key.append(audio[0]['key'])
    loudness.append(audio[0]['loudness'])
    mode.append(audio[0]['mode'])
    speechiness.append(audio[0]['speechiness'])
    acousticness.append(audio[0]['acousticness'])
    instrumentalness.append(audio[0]['instrumentalness'])
    liveness.append(audio[0]['liveness'])
    valence.append(audio[0]['valence'])
    tempo.append(audio[0]['tempo'])
    sleep(randint(1,3))
    
audioFeatures = pd.DataFrame({"title":title,
                        "artist":artist,
                        "danceability":danceability,
                        "energy":energy,
                        "key":key,
                        "loudness":loudness,
                        "mode":mode,
                        "speechiness":speechiness,
                        "acousticness":acousticness,
                        "instrumentalness":instrumentalness,
                        "liveness":liveness,
                        "valence":valence,
                        "tempo":tempo
                      })
'''

#Importing a saved copy of the songs with their audio features which I obtained with the instructions above
audioFeatures = pd.read_csv('TOPListsLarge.csv')
#Droping duplicates
audioFeatures = audioFeatures.drop_duplicates(['title'], keep='first')
#Creating a copy
audioFeatures2 = audioFeatures.copy()

#KMeans

#Splitting the 2
y = audioFeatures['title']
X_audio = audioFeatures.drop(['artist','title'], axis=1)
#Scaling X
X_prep = StandardScaler().fit_transform(X_audio)
#Aplying KMeans
kmeans = KMeans(n_clusters=4, random_state=1234)
kmeans.fit(X_prep)
clusters = kmeans.predict(X_prep)
#Creating a column with the cluster from each Song
audioFeatures2['cluster'] = clusters

#Code for obtaning the "Hot songs" list from playback.fm
'''
iterations = range(1900, 2011, 10)
[i for i in iterations]

pages = []

for i in iterations:
    # assemble the url:
    start_at= str(i)
    url = "https://playback.fm/one-hit-wonders-" + start_at + "s"

    # download html with a get request:
    response = requests.get(url)

    # monitor the process by printing the status code
    #print("Status code: " + str(response.status_code))

    # store response into "pages" list
    pages.append(response)

    # respectful nap:
    wait_time = randint(1,4)
    #print("I will sleep for " + str(wait_time) + " second/s.")
    sleep(wait_time)
    
from bs4 import BeautifulSoup
pages_parsed = []
titles = []
artists = []

for i in range(len(pages)):
    # parse all pages
    pages_parsed.append(BeautifulSoup(pages[i].content, "html.parser"))
    # select only the info about the songs
    songs_html = pages_parsed[i].select("div.content.post")
    # for song, store title and artist into lists
    for j in range(len(songs_html)):
        num_iter = len(songs_html[j].select("p.song-title a"))
        for k in range(num_iter):
            titles.append(songs_html[j].select("p.song-title a")[k].get_text())
            artists.append(songs_html[j].select("p.song-title strong")[k].get_text().strip())

#DF of "Hot songs"
topsongs = pd.DataFrame({"title":titles,
                              "artist":artists
                             })
#Droping duplicates 
topsongs = topsongs.drop_duplicates()
'''

#Importing a saved copy of the "Hot songs" which I obtained with the instructions above
topsongs = pd.read_csv('HOTSongs.csv')

#Looking for a Recomendation

#Asking for a Song
print("What is your song title?")
favSong = input()

#Looking for a Recomendation

#If it's in the "Hot songs" list, I will recommend another "Hot song"
if favSong in topsongs['title'].values: 
    RecSong = topsongs['title'].sample().to_string(index=False)
    print("Recommended song:", RecSong)
    #Looking for it on Spotify
    song = sp.search(q=RecSong, limit=1)
    if len(song['tracks']['items']) > 0:
        link = song["tracks"]["items"][0]['external_urls']['spotify']
        print("You can find it here:", link)
        
#If it's in the general list, I will recommend a song from its cluster    
elif favSong in audioFeatures2['title'].values:
    songRow = audioFeatures2[audioFeatures2.title == favSong]
    PossSongs = audioFeatures2[audioFeatures2.cluster == int(songRow.cluster.to_string(index=False))]
    RecSong = PossSongs['title'].sample().to_string(index=False)
    print("Recommended song:", RecSong)
    #Looking for it on Spotify
    song = sp.search(q=RecSong, limit=1)
    link = song["tracks"]["items"][0]['external_urls']['spotify']
    print("You can find it here:", link)
        
#If it isn't listed i will look for it on Spotify, cluster it and recommend a song from its cluster
else: 
    #Searching for the song and its audio features in Spotify
    song = sp.search(q=favSong, limit=1)
    song_uri = song["tracks"]["items"][0]["uri"] 
    audio = sp.audio_features(song_uri)
    #Checking if it exists and it has audio features:
    if ((len(song['tracks']['items']) > 0) & (len(audio)>0)):
        #Calculating its cluster
        SongAudioFeatures = SongAudioFeat(song, audio)
        cluster = int(cluster_for_a_Song(SongAudioFeatures, kmeans))
        #Recomending a song with the same cluster
        PossSongs = audioFeatures2[audioFeatures2.cluster == cluster]
        RecSong = PossSongs['title'].sample().to_string(index=False)
        print("Recommended song:", RecSong)
        #Looking for it on Spotify
        song = sp.search(q=RecSong, limit=1)
        link = song["tracks"]["items"][0]['external_urls']['spotify']
        print("You can find it here:", link)
    else: 
        print("Your song is not listed on Spotify or its audio features are not available")


