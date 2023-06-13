import streamlit as st
import pandas as pd
from PIL import Image

#@st.cache_data
# session state variables for smr data
if 'mean_all_img' not in st.session_state: # create session state
        st.session_state['mean_all_img'] = None
if 'median_all_img' not in st.session_state: # create session state
        st.session_state['median_all_img'] = None
if 'both_img' not in st.session_state: # create session state
        st.session_state['median_all_img'] = None
if 'mean_bin_img' not in st.session_state: # create session state
        st.session_state['median_all_img'] = None

if 'mean_epr' not in st.session_state: # create session state
        st.session_state['mean_epr'] = None
if 'median_epr' not in st.session_state: # create session state
        st.session_state['median_epr'] = None
if 'binned_epr' not in st.session_state: # create session state
        st.session_state['binned_epr'] = None

st.title('Cell Types')

st.write("Explore scRNA-seq data across 31 single cell types and 159 significant genes")

# load in EPR data
st.session_state['mean_epr'] = pd.read_csv('./data/exp_goi_celltypes_ord_mean.csv').rename({'Unnamed: 0': 'Gene'}, axis = 1)
st.session_state['median_epr'] = pd.read_csv('./data/exp_goi_celltypes_ord_median.csv').rename({'Unnamed: 0': 'Gene'}, axis = 1)
st.session_state['binned_epr'] = pd.read_csv('./data/binned_mean_epr.csv', index_col = 'Gene')

# load in image data
st.session_state['mean_all_img'] = Image.open('./data/all_mean.jpg')
st.session_state['median_all_img'] = Image.open('./data/all_median.jpg')
st.session_state['both_img'] = Image.open('./data/both_reduced.jpg')
st.session_state['mean_bin_img'] = Image.open('./data/mean_binned.jpg')

with st.container():
    st.header('Browse Data')
    with st.expander("Mean Expression Rank Percentiles"):
          st.dataframe(st.session_state['mean_epr'])
    with st.expander("Median Expression Rank Percentiles"):
          st.dataframe(st.session_state['median_epr'])
    with st.expander("Binned Mean Expression Rank Percentiles"):
          st.dataframe(st.session_state['binned_epr'])

with st.container():
    st.header('Image Gallery')
    image_pick = st.radio('Browse heatmaps', ('Mean Expression Percentile Rank', 'Median Expression Percentile Rank', 'Mean and Median Reduced Comparison', 'Binned Mean Expression Percentile Ranks'))

    if image_pick == 'Mean Expression Percentile Rank':
        st.image(st.session_state['mean_all_img'], caption = 'Mean Expression Percentile Rank (EPR)', use_column_width='auto')
    elif image_pick == 'Median Expression Percentile Rank':
        st.image(st.session_state['median_all_img'], caption = 'Median Expression Percentile Rank (EPR)', use_column_width='auto')
    elif image_pick == 'Mean and Median Reduced Comparison':
        st.image(st.session_state['both_img'], caption = 'Mean and Median Reduced Comparison (EPR). Genes with 0 median EPR excluded.', use_column_width='auto')
    elif image_pick == 'Binned Mean Expression Percentile Ranks':
        st.image(st.session_state['mean_bin_img'], caption = 'Binned Mean Expression Percentile Ranks (EPR). Excludes genes with only low expression (EPR < 10)', use_column_width='auto')
    else:
        print('Please select an option')