# Streamlit Home

# module load in
import streamlit as st
from PIL import Image

# Welcome message
st.title("OmicSynth Functional NDD Gene Browser")
st.header("""Our streamlit application has moved! Please click [here](https://omicsynth-streamlit-htco5r3hya-uc.a.run.app/) to be redirected""" )

# add CARD logo
card_img = Image.open('img/CARD-logo-white-print.png')
#dti_img = Image.open('img/dti_img.jpeg')

# updated DT logo
dti_img = Image.open('img/DT_logo.png')

st.image(card_img, width=400)
st.image(dti_img)

