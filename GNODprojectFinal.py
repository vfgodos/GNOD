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
import joblib

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
def cluster_for_a_Song(SongAudioFeatures, kmeans, scaler=joblib.load('scaler.bin')):
    #Splitting the DF
    y = SongAudioFeatures['title']
    X_audio = SongAudioFeatures.drop(['title'], axis=1)
    #Scaling X
    X_prep = scaler.transform(X_audio)
    #Aplying KMeans to calculate the cluster
    cluster = kmeansCreated.predict(X_prep)
    
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

#Code for obtaning the DF from Spotify API
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

#Getting a DF with the features I need

#I create a list with the Audio Features that I want to get
audioFeat = ['danceability','energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

#I create empty lists for the Features I want in my DF
title = []
artist = []
#Creating one empty list for each Audio Feature
for k in range(len(audioFeat)): 
    (locals()[audioFeat[k]]) = []

#With this first loop I get the general features and collect those which I need (title, artist)
for j in range(len(all_tracks)):
    title.append(all_tracks[j]["track"]["name"])
    artist.append(all_tracks[j]['track']['artists'][0]['name'])
    song_uri = all_tracks[j]["track"]["uri"]
    audio = sp.audio_features(song_uri)
    #With this second loop I get and collect the audio Features I need
    for i in range(len(audioFeat)): 
        (locals()[audioFeat[i]]).append(audio[0][audioFeat[i]])
        
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
scaler = StandardScaler()
X_prep = scaler.fit_transform(X_audio)
joblib.dump(scaler, 'scaler.bin')
#Aplying KMeans
kmeansCreated = KMeans(n_clusters=4, random_state=1234)
kmeansCreated.fit(X_prep)
clusters = kmeansCreated.predict(X_prep)
#Creating a column with the cluster from each Song
audioFeatures2['cluster'] = clusters

#
#Looking for a Recomendation
#

#Asking for a Song
print("What is your song title?")
favSong = input()


#Looking for a Recomendation
        
#If it's in the general list, I will recommend a song from its cluster    
if favSong in audioFeatures2['title'].values:
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
        cluster = int(cluster_for_a_Song(SongAudioFeatures, kmeansCreated))
        #Recomending a song with the same cluster
        PossSongs = audioFeatures2[audioFeatures2.cluster == cluster]
        RecSong = PossSongs['title'].sample().to_string(index=False)
        print("Recommended song:", RecSong)
        #Looking for it on Spotify
        song = sp.search(q=RecSong, limit=1)
        link = song["tracks"]["items"][0]['external_urls']['spotify']
        print("You can listen it here:", link)
        
        #Looking for an artist
        RecArtist = PossSongs['artist'].sample().to_string(index=False)
        artist = sp.search(q=RecArtist, limit=1)
        print("Recommended artist:", RecArtist)
        link = artist["tracks"]["items"][0]['external_urls']['spotify']
        print("You can listen one of his songs here:", link)
    else: 
        print("Your song is not listed on Spotify or its audio features are not available")