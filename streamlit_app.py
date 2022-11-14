from math import ceil
import streamlit as st
import scipy.io
import numpy as np
import librosa
import librosa.display
import sampling_studio_functions as functions

# ---------------------- Elements styling -------------------------------- #

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ------------------------- variables ---------------------------------- #
file_as_array = None
# ---------------------- Sidebar Elements -------------------------------- #

# # Browsing a file
label_col, browse_button_col = st.sidebar.columns(2)
with label_col:
    st.markdown("## Upload Signal")
with browse_button_col:
    file = st.file_uploader(
        "", type="wav", accept_multiple_files=False)

if file is not None:
    file_wav = librosa.load(file)
    file_as_array = np.asarray(file_wav[0])[:1000]
    functions.setSignalTime(file_wav[1])
else:
    functions.reset()


# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #
# # Add noise to signal

noise_flag = st.sidebar.checkbox("Noise", False)
if noise_flag:
    SNR_slider_value = st.sidebar.slider('SNR', 1, 100,50)
else:
    SNR_slider_value = 1

# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #

# # Add signals to the original signal
st.sidebar.header('Add Signals')

signal_frequency_slider_col,signal_amplitude_slider_col = st.sidebar.columns(2)

with signal_frequency_slider_col:
    signal_frequancy_slider = st.slider(
        'Frequency', 0.5, 20.0, 10.0, 0.1, format="%f")

with signal_amplitude_slider_col:
    signal_amplitude_slider = st.slider(
        'Amplitude', 0.1, 1.0, 0.1, 0.01, format="%f")

signal_phase_slider = st.sidebar.slider(
    'Phase', 0.0, 2.0, 0.0, 0.1, format="%fπ")

add_signal_button = st.sidebar.button("Add Signal", key="add_button")
if add_signal_button:
    functions.addSignalToList(signal_amplitude_slider, signal_frequancy_slider, signal_phase_slider)

# ------------------------------------------------------------------------ #

# # add signals to the selectbox
selectbox_signals_list = []
for signal in functions.getAddedSignalsList():
    selectbox_signals_list.append(
        f"Amp: {signal.amplitude:n} / Freq: {signal.frequency:n} / Phase: {signal.phase :n} π")
selected_signal = st.sidebar.selectbox("Signals", selectbox_signals_list)
selected_signal_split = str(selected_signal).split(" ")
if len(selected_signal_split) != 1:
    amplitude_slider = float(selected_signal_split[1])
    frequency_slider = float(selected_signal_split[4])
    phase_slider = float(selected_signal_split[7])

# ------------------------------------------------------------------------ #

# # Remove and clear signals from selectbox
remove_button_col, clear_button_col = st.sidebar.columns(2)
with remove_button_col:
    remove_signal_button = st.button("Remove", key="remove_button", disabled=len(
        functions.getAddedSignalsList()) <= 0)
    if remove_signal_button:
        functions.removeSignalFromList(
            amplitude=amplitude_slider, frequency=frequency_slider, phase=phase_slider)
        st.experimental_rerun()

with clear_button_col:
    clear_signals_button = st.button("Clear", key="clear_button", disabled=len(
        functions.getAddedSignalsList()) <= 0)
    if clear_signals_button:
        functions.reset()
        functions.clearAddedSignalsList()
        st.experimental_rerun()

# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #

# # Sampling
st.sidebar.header('Sampling')
normalized_sample_flag = st.sidebar.checkbox("Normalized", True)
if normalized_sample_flag:
    sampling_rate = st.sidebar.slider(
        'Nyquist rate Fs/Fmax', 1.5, 10.0, 2.5, 0.5, format="%f")
else:
    sampling_rate = st.sidebar.slider(
        'Fs', max(1.5, ceil(functions.f_max*0.5)*1.0), 5.0*functions.f_max, 2.0*float(functions.f_max), 0.5, format="%f")


# ----------------------- Main Window Elements --------------------------- #

website_title = '<p class="page_titel", style="font-family:Arial">Sampling Studio</p>'
st.markdown(website_title, unsafe_allow_html=True)
# ------------------------------------------------------------------------ #

functions.generate_sinusoidal(signal_amplitude_slider, signal_frequancy_slider, signal_phase_slider)
functions.generateResultedSignal(noise_flag, file_as_array, SNR_slider_value)
fig, Reconstructed_signal = functions.renderSampledSignal(
    sampling_rate, normalized_sample_flag)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------ #

# # Download the sampled signal

download = st.sidebar.button('Download Sampled Signal')
if download:
    st.sidebar.success("Downloaded")
    scipy.io.wavfile.write('signal.wav', 22025, np.array(
            Reconstructed_signal.index).astype(np.float32))
 
