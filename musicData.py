from song import Song
import pandas as pd
import os
spect_hash_list = []
melSpectroHashList = []
chroma = []
mfcc = []
Songs = []
for filename in os.listdir():
    if filename.endswith(".wav"):
        song = Song(filename)
        spectHash,firstHash,secondHash,thirdHash = song.getHash()
        Songs.append(filename)
        spect_hash_list.append(spectHash)
        melSpectroHashList.append(firstHash)
        chroma.append(secondHash)
        mfcc.append(thirdHash)
dict = {'song': Songs, 'spectrogram hash':spect_hash_list,\
    'mel spectrogram hash':melSpectroHashList,'chroma':chroma,'mfcc': mfcc}
df = pd.DataFrame(dict)
print(df.head)
df.to_csv('songsDataBase5.csv',index=False)