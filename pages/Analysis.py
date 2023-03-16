import streamlit as st
import pandas as pd
from scipy.stats import rankdata

@st.cache_data

def load_data(url, sheet_name="Sheet"):
    sh = st.session_state['client_auth'].open_by_url(url)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    return df

def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index = False)

def create_df(df, diseases, omics):
  # determine max possible options 
  dx_max = len(df['Disease'])
  o_max = len(df['Omic'].unique())

  # num of options in provided lists
  dx_len = len(diseases)
  o_len = len(omics)

  if dx_len == dx_max and o_max == o_len:
    return df

  elif dx_len == dx_max:
    new_df = df[df['Omic'].isin(omics)]
    return new_df

  elif o_max == o_len:
    new_df = df[df['Disease'].isin(diseases)]
    return new_df
  
  else:
    new_df = df.query("Disease in @diseases and Omic in @omics")
    return new_df

def fdr(df):
    
    # pull p_vals
    p_vals = df['p_SMR_multi']
    
    # run fdr on pvals
    ranked_p_values = rankdata(p_vals)
    fdr = p_vals * len(p_vals) / ranked_p_values
    fdr[fdr > 1] = 1
    
    # add column to df
    df['FDR_pval'] = fdr

    return df

def format_df(path, mtc = False):
    # format df
    df = pd.read_csv(path, sep = ',')
    
    # order columns
    cols_start = ['Omic', 'Disease', 'Gene','topRSID']
    df = df[[c for c in cols_start if c in df]
                      + [c for c in df if c not in cols_start]]
    
    if mtc:
        # run holm correction
        fdr_df = fdr(df)
        return fdr_df
    else:
        return df 

def zscore(df):
    df = df.copy()
    df['z_score'] = df.loc[:,'b_SMR']/df.loc[:,'se_SMR']

    return df

# CSS to inject contained in a string
hide_dataframe_row_index = """<style>.row_heading.level0 {display:none}.blank {display:none}</style>"""

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

# session state variables for smr data
if 'adj_data' not in st.session_state: # create session state
        st.session_state['adj_data'] = pd.DataFrame()
if 'sig5_data' not in st.session_state: # create session state
        st.session_state['sig5_data'] = pd.DataFrame()

# session state variables for filtered dataframe
if 'filterdf' not in st.session_state:
    st.session_state['filterdf'] = None
if 'filter_submit' not in st.session_state:
    st.session_state['filter_submit'] = False
if 'filter_name' not in st.session_state:
    st.session_state['filter_name'] = 'not_run'

# session state variables for multiple test correction
if 'mtc_status' not in st.session_state:
    st.session_state['mtc_status'] = 'not_run'
if 'mtc_df' not in st.session_state:
    st.session_state['mtc_df'] = None
if 'mtc_name' not in st.session_state:
    st.session_state['mtc_name'] = ''

# session state variables for z-score copmutation
if 'z_status' not in st.session_state:
    st.session_state['z_status'] = 'not_run'
if 'z_df' not in st.session_state:
    st.session_state['z_df'] = None
if 'z_name' not in st.session_state:
    st.session_state['z_name'] = ''

if isinstance(st.session_state['main_data'],pd.core.frame.DataFrame):
    main_df = st.session_state['main_data']
else:
    main_df = load_data(st.secrets['simple_sig'])

st.title('Data Analysis')

st.write("Here you can select from a variety of analysis methods used in our paper")

with st.form("Filter_Results"):
    st.write("Filter results by disease(s) and omic(s)")
    # diseases
    unique_dx = list(main_df['Disease'].unique())
    unique_dx.append('All')

    diseases = st.multiselect('Please select disease(s)', unique_dx)

    if "All" in diseases:
        diseases = list(main_df['Disease'].unique())

    st.write(f'**Selected Diseases**: {", ".join(diseases)}')

    # omics
    # preset list of NDD related omics
    ndd_omics = ['Brain_Amygdala', 'Brain_Hippocampus', 'Brain_Anterior_cingulate_cortex_BA24', 'Brain_Nucleus_accumbens_basal_ganglia', 'Brain_Hypothalamus',
    'Brain_Cerebellar_Hemisphere', 'Brain_Substantia_nigra', 'Brain_Caudate_basal_ganglia', 'Brain_Putamen_basal_ganglia', 'Brain_Cerebellum',  'Brain_Spinal_cord_cervical_c-1',
    'Brain_Cortex', 'Brain_Frontal_Cortex_BA9', 'Liver', 'Nerve_Tibial', 'Whole_Blood', 'Muscle_Skeletal', 'Cerebellum_metaBrain', 'Spinalcord_metaBrain', 'brain_eMeta', 'Cortex_metaBrain',
    'Basalganglia_metaBrain',  'Hippocampus_metaBrain', 'blood_eQTLgen', 'brain_mMeta', 'blood_Bryois', 'blood_mcrae', 'psychEncode_prefrontal_cortex', 'multiancestry']
    unique_omic = list(main_df['Omic'].unique())
    unique_omic.insert(0,'All')


    omics = st.multiselect('Please select omic(s)', unique_omic, help = 'Our NDD-related omics consist of omics related to brain areas, blood, and muscle/nerves.')

    if "All" in omics:
            omics = list(main_df['Omic'].unique())
    elif "NDD-related omics" in omics:
        omics = ndd_omics
    
    sig_opt = ['p < 0.05 & p_HEIDI > 0.01', 'p < 2.95E-06 & p_HEIDI > 0.01']
    sig_thresh = st.multiselect('Please select a significance threshold to apply', sig_opt, help = 'Thresholds used in analysis. For custom threshold please go to our data browser')


    submitted = st.form_submit_button("Filter Results!")
    
    if submitted:
        
        # p < 2.95e-06 threshold
        if sig_thresh == sig_opt[1]:
            adj_hits_df = load_data(st.secrets['adjusted_sig'])
            result_filter_df = create_df(adj_hits_df, diseases, omics)
            # add adj_df to session state
            st.session_state['sig5_data'] = adj_hits_df
            st.session_state['filterdf'] = result_filter_df       
            st.session_state['filter_submit'] = 'run' 
        # p < 0.05 threshold
        else:
            result_filter_df = create_df(main_df, diseases, omics)
            st.session_state['filterdf'] = result_filter_df       
            st.session_state['filter_submit'] = 'run'          

if st.session_state['filter_submit'] == 'run':
    st.dataframe(st.session_state['filterdf'])

    output_name = st.text_input('Please provide an output file name if you would like to download the results', placeholder = 'example.csv')
    st.session_state['filter_name'] = output_name
    if st.session_state['filter_name']:
        st.download_button(label="Download data as CSV", data=convert_df(st.session_state['filterdf']),file_name=output_name, mime='text/csv')

st.title('Analysis')
st.write(" Use your filtered data from above to run either multiple test correction, z-score calculation or both. If you would like to run these analysis on the whole dataset select 'All' for both the disease and omic choices above")

with st.container():
    col1, col2= st.columns(2)

    with col1:
        with st.form('MTC'): # form to run FDR adjustment
            st.subheader("Multiple Test Correction")
            st.write('Perform FDR test correction and add an "adjusted_pval" column. Correction will be calculated on the results from your **filtered dataframe**')
            
            mtc_run = st.form_submit_button("Run correction!")
            
            if mtc_run: # if run selection is pressed, run adjustment on filtered df
                
                try:
                    mtc_result = fdr(st.session_state['filterdf'])
                    st.session_state['mtc_df'] = mtc_result
                    st.session_state['mtc_status'] = 'run'
                except AttributeError:
                    st.error('Make sure to use the options above to filter your results and then run the correction')
                    st.session_state['mtc_status'] == 'not_run'  

        if st.session_state['mtc_status'] == 'run':
            st.dataframe(st.session_state['mtc_df'])
            mtc_filename = st.text_input('Please provide an output file name for the results of the correction', placeholder = 'example.csv')
            st.session_state['mtc_name'] = mtc_filename
            
            if st.session_state['mtc_name']:
                st.download_button(label="Download data as CSV", data=convert_df(st.session_state['mtc_df']),file_name=st.session_state['mtc_name'], mime='text/csv')

        with col2:
            with st.form('zscore'):
                st.subheader("Z-score")
                st.write('Compute z-score on your filtered dataframe and add a "z-score" column to your dataframe')

                z_run = st.form_submit_button("Compute z-scores!")

                if z_run:
                    try:
                        z_df = zscore(st.session_state['filterdf'])
                        st.session_state['z_df'] = z_df
                        st.session_state['z_status'] = 'run'
                    except TypeError:
                        st.error('Make sure to use the options above to filter your results and then run the computation')
                        st.session_state['z_status'] == 'not_run' 

            if st.session_state['z_status'] == 'run':
                st.dataframe(st.session_state['z_df'])
                z_filename = st.text_input('Please provide an output file name for the results of the z-score computation', placeholder = 'example.csv')
                st.session_state['z_name'] = z_filename
                
                if st.session_state['z_name']:
                    st.download_button(label="Download data as CSV", data=convert_df(st.session_state['z_df']),file_name=st.session_state['z_name'], mime='text/csv')
