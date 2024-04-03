# Streamlit Home

# module load in
import streamlit as st
import pandas as pd
import gspread 
from gspread_pandas import Spread, Client
from google.oauth2.service_account import Credentials
from PIL import Image
from st_files_connection import FilesConnection


# Welcome message
st.title("OmicSynth Functional NDD Gene Browser")
st.markdown("""Our streamlit application has moved! Please click [here](https://omicsynth-streamlit-htco5r3hya-uc.a.run.app/) to be redirected""" )

# add CARD logo
card_img = Image.open('img/CARD-logo-white-print.png')
#dti_img = Image.open('img/dti_img.jpeg')

# updated DT logo
dti_img = Image.open('img/DT_logo.png')

st.sidebar.image(card_img)
st.sidebar.image(dti_img)

