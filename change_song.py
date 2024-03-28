import warnings
import psycopg2
from io import BytesIO
from diffusers.configuration_utils import ConfigMixin, register_to_config
from diffusers.schedulers.scheduling_utils import SchedulerMixin
from scipy.io import wavfile
import soundfile as sf
import os
warnings.filterwarnings("ignore")
import sys
from generation_utilities import *

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import shutil
import torch
from IPython.display import Audio
from audiodiffusion import AudioDiffusion, AudioDiffusionPipeline
from audiodiffusion.audio_encoder import AudioEncoder
import librosa
import librosa.display

import IPython.display as ipd

device = "cuda" if torch.cuda.is_available() else "cpu"

# audio_diffusion = AudioDiffusionPipeline.from_pretrained("teticio/latent-audio-diffusion-256").to(device)
audio_diffusion = AudioDiffusionPipeline.from_pretrained("SAint7579/orpheus_ldm_model_v1-0").to(device)
ddim = AudioDiffusionPipeline.from_pretrained("teticio/audio-diffusion-ddim-256").to(device)





try:
    import librosa  # noqa: E402

    _librosa_can_be_imported = True
    _import_error = ""
except Exception as e:
    _librosa_can_be_imported = False
    _import_error = (
        f"Cannot import librosa because {e}. Make sure to correctly install librosa to be able to install it."
    )


class Mel(ConfigMixin, SchedulerMixin):
    """
    Parameters:
        x_res (`int`): x resolution of spectrogram (time)
        y_res (`int`): y resolution of spectrogram (frequency bins)
        sample_rate (`int`): sample rate of audio
        n_fft (`int`): number of Fast Fourier Transforms
        hop_length (`int`): hop length (a higher number is recommended for lower than 256 y_res)
        top_db (`int`): loudest in decibels
        n_iter (`int`): number of iterations for Griffin Linn mel inversion
    """

    config_name = "mel_config.json"

    @register_to_config
    def __init__(
        self,
        x_res: int = 256,
        y_res: int = 256,
        sample_rate: int = 22050,
        n_fft: int = 2048,
        hop_length: int = 512,
        top_db: int = 80,
        n_iter: int = 32,
    ):
        self.hop_length = hop_length
        self.sr = sample_rate
        self.n_fft = n_fft
        self.top_db = top_db
        self.n_iter = n_iter
        self.set_resolution(x_res, y_res)
        self.audio = None

        if not _librosa_can_be_imported:
            raise ValueError(_import_error)

    def set_resolution(self, x_res: int, y_res: int):
        """Set resolution.

        Args:
            x_res (`int`): x resolution of spectrogram (time)
            y_res (`int`): y resolution of spectrogram (frequency bins)
        """
        self.x_res = x_res
        self.y_res = y_res
        self.n_mels = self.y_res
        self.slice_size = self.x_res * self.hop_length - 1

    def load_audio(self, audio_file: str = None, raw_audio: np.ndarray = None):
        """Load audio.

        Args:
            audio_file (`str`): must be a file on disk due to Librosa limitation or
            raw_audio (`np.ndarray`): audio as numpy array
        """
        if audio_file is not None:
            self.audio, _ = librosa.load(audio_file, mono=True, sr=self.sr)
        else:
            self.audio = raw_audio

        # Pad with silence if necessary.
        if len(self.audio) < self.x_res * self.hop_length:
            self.audio = np.concatenate([self.audio, np.zeros((self.x_res * self.hop_length - len(self.audio),))])

    def get_number_of_slices(self) -> int:
        """Get number of slices in audio.

        Returns:
            `int`: number of spectograms audio can be sliced into
        """
        return len(self.audio) // self.slice_size

    def get_audio_slice(self, slice: int = 0) -> np.ndarray:
        """Get slice of audio.

        Args:
            slice (`int`): slice number of audio (out of get_number_of_slices())

        Returns:
            `np.ndarray`: audio as numpy array
        """
        return self.audio[self.slice_size * slice : self.slice_size * (slice + 1)]

    def get_sample_rate(self) -> int:
        """Get sample rate:

        Returns:
            `int`: sample rate of audio
        """
        return self.sr

    def audio_slice_to_image(self, slice: int, ref=np.max) -> Image.Image:
        """Convert slice of audio to spectrogram.

        Args:
            slice (`int`): slice number of audio to convert (out of get_number_of_slices())

        Returns:
            `PIL Image`: grayscale image of x_res x y_res
        """
        S = librosa.feature.melspectrogram(
            y=self.get_audio_slice(slice), sr=self.sr, n_fft=self.n_fft, hop_length=self.hop_length, n_mels=self.n_mels
        )
        log_S = librosa.power_to_db(S, ref=ref, top_db=self.top_db)
        bytedata = (((log_S + self.top_db) * 255 / self.top_db).clip(0, 255) + 0.5).astype(np.uint8)
        image = Image.fromarray(bytedata)
        return image

    def image_to_audio(self, image: Image.Image) -> np.ndarray:
        """Converts spectrogram to audio.

        Args:
            image (`PIL Image`): x_res x y_res grayscale image

        Returns:
            audio (`np.ndarray`): raw audio
        """
        bytedata = np.frombuffer(image.tobytes(), dtype="uint8").reshape((image.height, image.width))
        log_S = bytedata.astype("float") * self.top_db / 255 - self.top_db
        S = librosa.db_to_power(log_S)
        audio = librosa.feature.inverse.mel_to_audio(
            S, sr=self.sr, n_fft=self.n_fft, hop_length=self.hop_length, n_iter=self.n_iter
        )
        return audio

def audioarray_to_mp3(audioarray, file_path):
    sample_rate = 22050
    mel = Mel()
    # Save the audio array as a temporary WAV file
    temp_wav_file = "temp.wav"
    wavfile.write(temp_wav_file, sample_rate, audioarray)

    # Set the output MP3 file path
    os.remove(file_path)
    output_mp3_file = file_path

    # Load the temporary WAV file
    wav_data, sr = sf.read(temp_wav_file)

    # Convert the WAV data to MP3 format
    sf.write(output_mp3_file, wav_data, sample_rate, format="MP3")
    
    return None

def audioarray_to_mp3_highdb(audioarray, file_path):
    sample_rate = 22050
    # Save the audio array as a temporary WAV file
    temp_wav_file = "temp.wav"

    audio = ipd.Audio(audioarray, rate=sample_rate)

    ## Write file into a wav file with open
    with open(file_path, 'wb') as f:
        f.write(audio.data)
        
    return None


def main():
    # # Connect to the PostgreSQL database
    # conn = psycopg2.connect(database="orpheus", user="postgres", password="1234", host="localhost", port="5432")
    # cur = conn.cursor()

    # # Assuming you have a table named 'images' with columns 'id' (serial primary key) and 'image_data' (bytea)
    # table_name = "songs"
    
    # image_id = np.random.randint(1, 10)  # Replace with the actual ID of the image you want to retrieve
    # print(image_id)
    # # Retrieve the image data from the database
    # cur.execute(f"SELECT song FROM {table_name} WHERE id = %s", (image_id,))
    # result = cur.fetchone()

    # # Convert the bytea data to PIL.Image.Image object
    # image_bytes = BytesIO(result[0])
    # image = Image.open(image_bytes)
    # # image.save("C:/VS code projects/Orpheus-2/audio/thumbnail.png")
    # # Close the database connection
    # cur.close()
    # conn.close()
    
    # getting the song names
    song1_name=sys.argv[1]
    song2_name=sys.argv[2]
    song3_name=sys.argv[3]
    similarity_index=float(sys.argv[4])/100
    print("Similarity index is",similarity_index)
    print("Song1 name is",song1_name)
    print("Song2 name is",song2_name)
    print("Song3 name is",song3_name)
    print("Similarity index is",similarity_index)
    #
    mel = Mel()
    # audioarray_to_mp3(mel.image_to_audio(image), "audio/output.mp3")
    # song_array_1, sr = librosa.load("audio\output.mp3", sr=22050)
    # song_array_1 = song_array_1[:sr*5]
    
    input_songs_array = []
    
    if song1_name != "None":
        song_array_1, sr = librosa.load(f"input_songs/{song1_name}.mp3", sr=22050)
        input_songs_array.append(song_array_1)
    # song_array_1, sr = librosa.load(f"input_songs/{song1_name}.mp3", sr=22050)
    
    # song_array_1 = song_array_1[:sr*5]
    if song2_name != "None":
        song_array_2, sr = librosa.load(f"input_songs/{song2_name}.mp3", sr=22050)
        input_songs_array.append(song_array_2)
    
    # song_array_2, sr = librosa.load(f"input_songs/{song2_name}.mp3", sr=22050)
    # song_array_2 = song_array_2[:sr*5]
    
    if song3_name != "None":
        song_array_3, sr = librosa.load(f"input_songs/{song3_name}.mp3", sr=22050)
        input_songs_array.append(song_array_3)
    # song_array_3, sr = librosa.load(f"input_songs/{song3_name}.mp3", sr=22050)
    # song_array_3 = song_array_3[:sr*5]
    mage, audio = generate_songs(input_songs_array, similarity=similarity_index, quality=200)
    mage.save("audio/thumbnail.png")
    audioarray_to_mp3_highdb(audio,"audio/generated_song.mp3")
    # if i==3:
    #     shutil.copy2("aidio/nvg.mp3", "audio/generated_song.mp3")
    
    print("Python script executed successfully")

if __name__ == "__main__":
    main()