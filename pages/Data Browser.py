# enable user to browse raw data
from turtle import down
import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from scipy.stats import rankdata

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

if 'filterdf' not in st.session_state:
        st.session_state['filterdf'] = None
if 'filter_submit' not in st.session_state:
    st.session_state['filter_submit'] = False

if isinstance(st.session_state['main_data'],pd.core.frame.DataFrame):
    main_df = st.session_state['main_data']
else:
    main_df = load_data(st.secrets['simple_sig'])

st.title('Data Browser')

st.write("Here you can select data based on a specified disease and omic list. The interactive table allows users to select custom filters for all columns. You may also export your filtered results as a csv file.")

with st.container():
    with st.form("Filter_Results"):
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
        unique_omic.insert(1,'NDD-related omics')

        omics = st.multiselect('Please select omic(s)', unique_omic, help = 'Our NDD-related omics consist of omics related to brain areas, blood, and muscle/nerves.')

        if "All" in omics:
            omics = list(main_df['Omic'].unique())
        elif "NDD-related omics" in omics:
            omics = ndd_omics


        submitted = st.form_submit_button("Filter Results!")
        st.session_state['filter_submit'] = submitted
        if submitted:
            result_filter_df = create_df(main_df, diseases, omics)
            st.session_state['filterdf'] = result_filter_df            

with st.container():
    # You can call any Streamlit command, including custom components:
    if st.session_state['filter_submit']:
        gb = GridOptionsBuilder.from_dataframe(st.session_state['filterdf'])
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        gridOptions = gb.build()

        grid_response = AgGrid(
            st.session_state['filterdf'],
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            theme='streamlit', #Add theme color to the table
            enable_enterprise_modules=True,
            height=500, 
            width=750,
            reload_data=True
        )

        data = grid_response['data']
        selected = grid_response['selected_rows'] 
        df = pd.DataFrame(selected)

        # allow user to download their filtered output
        output_name = st.text_input('Please provide an output file name if you would like to download your filtered results as a CSV file', placeholder = 'example.csv')
        if output_name:
            st.download_button(label="Download data as CSV", data=convert_df(st.session_state['filterdf']),file_name=output_name, mime='text/csv')