# import sys
# sys.path.append('../')

# import streamlit as st
# import librosa
# import soundfile as sf
# import generation_utilities

# import os
# os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# st.title("Song Generation")



# button = st.button("Generate")

# if button:
#     st.write("Generating...")
#     song_list = [librosa.load(f"../input_songs/{song}.mp3", sr=22050)[0] for song in ["22", "Anti-Hero", "Back-to-december","Blank-Space","Cardigan","Delicate","Lover","Love-Story","Willow","You-Belong-With-Me"]]
#     spectrogram, generated_song = generation_utilities.generate_songs([song_list[0]], similarity=0.9, quality=500, merging_quality=100, device='cuda')
#     st.write("Generated!")
    
#     generated_audio_path = "generated_audio.wav"
#     sf.write(generated_audio_path, generated_song, 22050)
    
#     # Display the generated audio
#     st.audio(generated_audio_path, format='audio/wav')
import streamlit as st
import sys
sys.path.append('../')
import generation_utilities
import numpy as np
import librosa
from glob import glob
import random
import IPython.display as ipd
import soundfile as sf
import importlib
import ipywidgets as widgets
import numpy as np
importlib.reload(generation_utilities)

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


if 'song_name' not in st.session_state:
    st.session_state['song_name'] = None
if 'similarity' not in st.session_state:
    st.session_state['similarity'] = None


form1 = st.form(key="form1")
song_options = form1.multiselect("Select songs from library",["22", "Anti-Hero", "Back-to-december","Blank-Space","Cardigan","Delicate","Lover","Love-Story","Willow","You-Belong-With-Me"])
similarity = form1.slider("Similarity", 0.0, 1.0, 0.9)
submit = form1.form_submit_button("Submit")

if submit:
    song_list = [librosa.load(f"../input_songs/{song}.mp3", sr=22050)[0] for song in song_options]
    print(song_options)
    
    spectrogram, generated_song = generation_utilities.generate_songs(song_list, similarity=similarity, quality=500, merging_quality=100, device='cuda')
    st.session_state['song_name'] = song_options[0]
    st.session_state['similarity'] = similarity
    
    # saving temps
    sf.write(f"temp.wav", generated_song, 22050)
    np.save("temp.npy", spectrogram)
    st.switch_page("pages/page2.py")
    # st.audio(generated_song, format='audio/wav',sample_rate=22050)
    
    # generated_audio_path = "generated_audio.wav"
    # sf.write(generated_audio_path, generated_song, 22050)
    # st.audio(generated_audio_path, format='audio/wav')
    # st.write("Generated!")