import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection

@st.cache_data
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index = False)

def load_data(url, in_format = 'csv'):
    # establish connection
    conn = st.experimental_connection('gcs', type=FilesConnection)

    # read in file
    df = conn.read(url, input_format=in_format)
    return df

# pull main df with SMR data
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = load_data(st.secrets['all_associations'], 'parquet')

# pull all sig (p < 0.05) SMR data (NOT ADJUSTED)
if 'mainsig_data' not in st.session_state:
    st.session_state['mainsig_data'] = load_data(st.secrets['simple_sig'])

# df for drug database data
if 'drugdf' not in st.session_state:
    st.session_state['drugdf'] = load_data(st.secrets['drug_db'])

if 'sig5_data' not in st.session_state:
    st.session_state['sig5_data'] = load_data(st.secrets['adjusted_sig'])

st.title('Data Download')
st.write('Download source data. Data is also available on [Google Drive](https://drive.google.com/drive/u/0/folders/1W2vec0eMWcnhSGFqcmjICLIfUiTPJsIY)')
st.subheader('SMR results')
# allow user to download results
st.write('1. Download all unfilitered SMR associations')
st.download_button(label="Unfilitered SMR associations as CSV", data=convert_df(st.session_state['main_data']), mime='text/csv')
st.markdown('2. Download all significant SMR associations (p<sub>SMRmulti</sub> < 0.05 & p<sub>HEIDI</sub> > 0.01)', unsafe_allow_html = True)
st.download_button(label="Significant SMR associations as CSV", data=convert_df(st.session_state['mainsig_data']), mime='text/csv')
st.markdown('3. Download all adjusted significant SMR associations (p<sub>SMRmulti</sub> < 2.95E-06 & p<sub>HEIDI</sub> > 0.01)', unsafe_allow_html = True)
st.download_button(label="Adjusted significant SMR associations as CSV", data=convert_df(st.session_state['sig5_data']), mime='text/csv')


st.subheader('Druggable Genes Data')
st.write('Download druggable genes and drugs data')
st.download_button(label="Drug database", data=convert_df(st.session_state['drugdf']), mime='text/csv')