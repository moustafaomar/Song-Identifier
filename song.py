from pydub import AudioSegment
import numpy as np
from scipy.io.wavfile import write
import csv
import librosa 
import imagehash
from PIL import Image
from scipy import signal
import logging
logging.basicConfig(filename="logging.log", format='%(asctime)s %(message)s', filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 
class Song:
    def __init__(self, location=None):
        self.path = location
        if self.path is None:
            self.data = None
            return
        self.getSongFromPath()
    def loadSong(self,location):
        self.path = location
        if(self.getSongFromPath()): 
            return self.data
        else:
            return None
    def getSongFromPath(self):
        logger.debug('Loading song on path %s',self.path)
        audiofile = AudioSegment.from_mp3(self.path)[:60000] 
        self.data = np.array(audiofile.get_array_of_samples()[:2600000])
        self.rate = audiofile.frame_rate
    def mix(self,song,factor):
        logger.debug('Mixing driver called with value %s on song %s',factor,song)
        factor = factor/100
        mix = self.data*factor + song.data*(1-factor)
        output=mix.astype(np.int16)
        write("mix.wav", 48000, output)
    def getSimilarity(self):
        SongspectHash,SongfirstHash,SongsecondHash,SongthirdHash=self.getHash()
        FinalList = self.similarity(SongspectHash,SongfirstHash,SongsecondHash,SongthirdHash)
        return FinalList
    def similarity(self,SongspectHash,SongfirstHash,SongsecondHash,SongthirdHash):
        FinalList=[]
        with open('songsDataBase5.csv') as csv_file:
            logger.debug('DB loaded successfully')
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    index=(abs(imagehash.hex_to_hash(row[1])-imagehash.hex_to_hash(SongspectHash))+abs(imagehash.hex_to_hash(row[2])-imagehash.hex_to_hash(SongfirstHash))+abs(imagehash.hex_to_hash(row[3])-imagehash.hex_to_hash(SongsecondHash))+abs(imagehash.hex_to_hash(row[4])-imagehash.hex_to_hash(SongthirdHash)))/255
                    FinalList.append([index/4,row[0]])
            for i in FinalList:
                i[0]= 100*abs(1-i[0])
        return FinalList
    def getHash(self):
        mp3_audio = AudioSegment.from_file((self.path), format="mp3")[:60000]  # read mp3
        wavsong = np.array(mp3_audio.get_array_of_samples()[:2600000]).astype(np.float16)
        samplingFrequency = mp3_audio.frame_rate
        return self.Hash(wavsong,samplingFrequency)
    def Hash(self,wavsong,samplingFrequency):
        _,_,colorMesh =signal.spectrogram(wavsong,fs=samplingFrequency)
        feature1= librosa.feature.melspectrogram(y=wavsong,sr=samplingFrequency)
        feature2= librosa.feature.chroma_stft(y=wavsong,sr=samplingFrequency)
        feature3= librosa.feature.mfcc(y=wavsong,sr=samplingFrequency)
        spect_image=Image.fromarray(colorMesh)
        new_image = Image.fromarray(feature1)
        new_image2 = Image.fromarray(feature2)
        new_image3 = Image.fromarray(feature3)
        spectHash=imagehash.phash(spect_image, hash_size=16).__str__()
        firstHash=imagehash.phash(new_image, hash_size=16).__str__()
        secondHash=imagehash.phash(new_image2, hash_size=16).__str__()
        thirdHash=imagehash.phash(new_image3, hash_size=16).__str__()
        logger.debug('Hashes generated successfully')
        return spectHash,firstHash,secondHash,thirdHash