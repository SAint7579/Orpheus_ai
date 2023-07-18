import torch
from IPython.display import Audio
from audiodiffusion import AudioDiffusion, AudioDiffusionPipeline
from audiodiffusion.audio_encoder import AudioEncoder
import librosa
import librosa.display
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"

audio_diffusion = AudioDiffusionPipeline.from_pretrained("teticio/latent-audio-diffusion-256").to(device)
ddim = AudioDiffusionPipeline.from_pretrained("teticio/audio-diffusion-ddim-256").to(device)

### Add numpy docstring to generate_from_music
def generate_from_music(song_array, diffuser, start_step, total_steps=100, device="cuda"):
    """
    Generates audio from a given song array using a given diffuser.
    Parameters
    ----------
    song_array : numpy.ndarray
        The song array to use as the raw audio.
    diffuser : AudioDiffusionPipeline
        The diffuser to use to generate the audio.
    start_step : int
        The step to start generating from.
    total_steps : int
        The total number of steps to generate.
    device : str
        The device to use for generation.
    Returns
    -------
    numpy.ndarray
        The generated audio.
    """
    generator = torch.Generator(device=device)
    generator.seed()
    output = diffuser(raw_audio=song_array, generator = generator, start_step=start_step, steps=total_steps)
    return output.images[0], output.audios[0, 0]

def generate_from_music_long(song_array, diffuser, start_step, total_steps=100, device="cuda"):
    """
    Generates a 10 second audio from a given song array using a given diffuser.
    Parameters
    ----------
    song_array : numpy.ndarray
        The song array to use as the raw audio.
    diffuser : AudioDiffusionPipeline
        The diffuser to use to generate the audio.
    start_step : int
        The step to start generating from.
    total_steps : int
        The total number of steps to generate.
    device : str
        The device to use for generation.
    Returns
    -------
    numpy.ndarray
        The generated audio.
    """
    generator = torch.Generator(device=device)
    generator.seed()
    output = diffuser(raw_audio=song_array, generator = generator, start_step=start_step, steps=total_steps)

    # Get the track and use the diffuser again to create the continuation
    track = output.audios[0, 0]
    sample_rate = diffuser.mel.get_sample_rate()
    overlap_secs = 2
    overlap_samples = overlap_secs * sample_rate

    continue_output = diffuser(raw_audio=track[-overlap_samples:],
                               generator=generator,
                               start_step=start_step,
                               mask_start_secs=overlap_secs)
    # image2 = output.images[0]
    audio2 = continue_output.audios[0, 0]
    track = np.concatenate([track, audio2[overlap_samples:]])

    return output.images[0], track


## Add docstring to iterative_slerp function in numpy format
def iterative_slerp(song_arrays, ddim, steps=10):
    """Iterative slerp function.

    Parameters
    ----------
    song_arrays : list
        List of song arrays to slerp.
    ddim : AudioDiffusion ddim model
        AudioDiffusion object.

    Returns
    -------
    slerp : torch.Tensor
        Slerped tensor.
    """
    noise = []
    for arr in song_arrays:
        ddim.mel.audio = arr
        noise.append(ddim.encode([ddim.mel.audio_slice_to_image(0)], steps=steps))

    slerp = noise[0]
    for i in range(1, len(noise)):
        slerp = ddim.slerp(slerp, noise[i], 0.5)

    return slerp

def merge_songs(song_arrays, ddim, slerp_steps=10, diffusion_steps=100, device="cuda"):
    """Merge songs.

    Parameters
    ----------
    song_arrays : list
        List of song arrays to merge.
    ddim : AudioDiffusion ddim model
        AudioDiffusion object.

    Returns
    -------
    spectrogram : np.ndarray
        Merged spectrogram.
    audio : np.ndarray
        Merged audio.
    """
    generator = torch.Generator(device=device)
    generator.manual_seed(7579)
    slerp = iterative_slerp(song_arrays, ddim, slerp_steps)
    merged = ddim(noise=slerp, generator=generator, steps=diffusion_steps)
    return merged.images[0], merged.audios[0, 0]

## Write generate songs function with numpy docstring
def generate_songs(conditioning_songs, similarity=0.9, quality=500, merging_quality=100, device='cuda'):
    """Generate songs.

    Parameters
    ----------
    conditioning_songs : list
        List of conditioning songs.
    similarity : float
        Similarity between conditioning songs.
    quality : int
        Quality of generated song.

    Returns
    -------
    spec_generated : np.ndarray
        Spectrogram of generated song.
    generated : np.ndarray
        Generated song.
    """
    ## Merging songs
    print("Merging songs...")
    if len(conditioning_songs)>1:
        print(conditioning_songs)
        for c in conditioning_songs:
            print(len(c))
        spec_merged, merged = merge_songs(conditioning_songs, ddim, slerp_steps=merging_quality, diffusion_steps=merging_quality, device=device)
    else:
        merged = conditioning_songs[0]

    ## Take a random 10 second slice from the merged song
    # sample_rate = ddim.mel.get_sample_rate()
    # start = np.random.randint(0, len(merged) - 5 * sample_rate)
    # merged = merged[start:start + 5 * sample_rate]


    print("Generating song...")
    ## quality = X - similarity*X
    total_steps = min([1000, int(quality/(1-similarity))])
    start_step = int(total_steps*similarity)
    spec_generated, generated = generate_from_music(merged, audio_diffusion, start_step=start_step, total_steps=total_steps, device=device)

    return spec_generated, generated

# if __name__ == '__main__':
#     song1 = "D:/Projects/Orpheus_ai/DataSet/Sep_Dataset/accompaniment/000010.mp3"
#     song2 = "D:/Projects/Orpheus_ai/DataSet/Sep_Dataset/accompaniment/000002.mp3"
#     song3 = "D:/Projects/Orpheus_ai/DataSet/Sep_Dataset/accompaniment/000003.mp3"

#     song_array_1, sr = librosa.load(song1, sr=22050)
#     song_array_1 = song_array_1[:sr*5]

#     song_array_2, sr = librosa.load(song2, sr=22050)
#     song_array_2 = song_array_2[:sr*10]

#     song_array_3, sr = librosa.load(song3, sr=22050)
#     song_array_3 = song_array_3[:sr*10]

#     generator = torch.Generator(device=device)

#     # seed = 239150437427
#     image, audio = generate_songs([song_array_2, song_array_3], similarity=0.5, quality=10, device=device)
#     Audio(audio, rate=sr)