# Streamlit Home

# module load in
import streamlit as st
import pandas as pd
import gspread 
from gspread_pandas import Spread, Client
from google.oauth2.service_account import Credentials
from PIL import Image

if 'client_auth' not in st.session_state: # create session state variable for client auth 
        st.session_state['client_auth'] = None
# load in main df and keep in cache to mitigate reloading on every page
if 'main_data' not in st.session_state: # create session state
        st.session_state['main_data'] = pd.DataFrame()

scopes = ["https://www.googleapis.com/auth/spreadsheets",]

skey = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)

# add auth keys to session state
st.session_state['client_auth'] = client

@st.cache_data(show_spinner = False)

def load_data(url, sheet_name="Sheet"):
    sh = client.open_by_url(url)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    return df

# load in unfiltered associations
def create_main():
    df = load_data(st.secrets['simple_sig'])

    return df

# Welcome message
st.title("OmicSynth Functional NDD Gene Browser")
st.markdown("""Welcome to OmicSynth's Neurodegenerative Disorders functionl analysis browser!
            This application allows you to browse SMR data from our manuscript and conduct customized analysis. 
            Please report any issues, provide feedback, or ask general questions to chelsea.alvarado@nih.gov""" )


with st.spinner('Loading in data ... only happens once :)'):
    main_df = create_main()
    st.session_state['main_data'] = main_df
    st.success('Done!')

# add CARD logo
card_img = Image.open('img/CARD-logo-white-print.png')
dti_img = Image.open('img/dti_img.jpeg')

st.sidebar.image(card_img)
st.sidebar.image(dti_img)

