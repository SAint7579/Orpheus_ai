import streamlit as st
import glob
import soundfile as sf
import shutil
import sys
sys.path.append('../../')
spectrograms = glob.glob("temp*.npy")
generated_songs = glob.glob("temp*.wav")
st.audio(generated_songs[0], format='audio/wav',sample_rate=22050)
rating = st.slider("Rating", 0, 5, 0)
submit_rating = st.button("Submit Rating")

if submit_rating:
    shutil.copy(generated_songs[0],f"../DataSet/Song/{st.session_state['song_name']}_{st.session_state['similarity']}_{rating}.wav")
    shutil.copy(spectrograms[0],f"../DataSet/Spec/{st.session_state['song_name']}_{st.session_state['similarity']}_{rating}.npy")
    st.switch_page("main.py")
