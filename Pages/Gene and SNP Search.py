import streamlit as st
import pandas as pd

#@st.cache(show_spinner=False)

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

def pull_snp_count(input_df, p_smr_multi = None, p_HEIDI = None, count = False, *snps):
    # filter df for user defined p_values if provided
    if p_smr_multi != None and p_HEIDI != None:
        filter_df = input_df.query(f'p_SMR_multi < {p_smr_multi} & p_SMR_multi != -9999.000000 & p_HEIDI > {p_HEIDI} & p_HEIDI != -9999.000000')
    else:
        filter_df = input_df.query('p_SMR_multi != -9999.000000 & p_HEIDI != -9999.000000')

    # narrow down to main columns of interest
    filter_df = filter_df[['Omic', 'Disease', 'Gene_rename', 'topRSID', 'b_GWAS','p_GWAS', 'b_SMR', 'p_SMR_multi', 'p_HEIDI']]
    
    # filter for genes
    final_df = pd.DataFrame()
    for snps in snps:
        df = filter_df.query(f"topRSID == '{snps}'")
        final_df = pd.concat([final_df,df])
    
    final_df.sort_values('p_HEIDI', ascending = False, inplace = True)
    final_df_fil = final_df.set_index(['topRSID', 'Disease', 'Omic']).sort_index()
    
    if count == True:
        final_df.sort_values('Omic', ascending = False, inplace = True)
        final_df_count = final_df.groupby(['topRSID', 'Omic']).count()
        return final_df_fil, final_df_count
    else:
        return final_df_fil

def pull_genes_count(input_df, p_smr_multi = None, p_HEIDI = None, count = False, *genes):
    # filter df for user defined p_values if provided
    if p_smr_multi != None and p_HEIDI != None:
        filter_df = input_df.query(f'p_SMR_multi < {p_smr_multi} & p_SMR_multi != -9999.000000 & p_HEIDI > {p_HEIDI} & p_HEIDI != -9999.000000')
    else:
        filter_df = input_df.query('p_SMR_multi != -9999.000000 & p_HEIDI != -9999.000000')
    # narrow down to main columns of interest
    filter_df = filter_df[['Omic', 'Disease', 'Gene', 'topRSID', 'b_GWAS','p_GWAS', 'b_SMR', 'p_SMR_multi', 'p_HEIDI']]
    
    # filter for genes
    final_df = pd.DataFrame()
    for gene in genes:
        df = filter_df.query(f"Gene == '{gene}'")
        final_df = pd.concat([final_df,df])
    
    final_df.sort_values('p_HEIDI', ascending = False, inplace = True)
    final_df_fil = final_df.set_index(['Gene', 'Disease', 'Omic']).sort_index()
    
    if count == True:
        final_df.sort_values('Omic', ascending = False, inplace = True)
        final_df_count = final_df.groupby(['Gene', 'Omic']).count()
        return final_df_fil, final_df_count
    else:
        return final_df_fil


# session state variables for SNP dataframe
if 'snps_list' not in st.session_state: # genes in dataase
    st.session_state['snps_list'] = None
if 'snp_results_df' not in st.session_state:
    st.session_state['snp_results_df'] = None

# session state variables for  gene dataframe
if 'genes_list' not in st.session_state: # genes in dataase
    st.session_state['genes_list'] = None
if 'gene_results_df' not in st.session_state:
    st.session_state['gene_results_df'] = None

# session state variables for parameter buttons

if 'omic_count_gene' not in st.session_state:
    st.session_state['omic_count_gene'] = False
if 'dx_count_gene' not in st.session_state:
    st.session_state['dx_count_gene'] = False

# session state variables for count dfs
if 'omic_count_gene' not in st.session_state:
    st.session_state['omic_count_gene'] = False
if 'dx_count_gene' not in st.session_state:
    st.session_state['dx_count_gene'] = False

if 'omic_df_snp' not in st.session_state:
    st.session_state['omic_df_snp'] = False
if 'dx_df_snp' not in st.session_state:
    st.session_state['dx_df_snp'] = False

if 'omic_df_gene' not in st.session_state:
    st.session_state['omic_df_gene'] = False
if 'dx_df_gene' not in st.session_state:
    st.session_state['dx_df_gene'] = False

# parameter session state
if 'pval' not in st.session_state:
    st.session_state['pval'] = 0.05
if 'heidi' not in st.session_state:
    st.session_state['heidi'] = 0.01
if 'snps' not in st.session_state:
    st.session_state['snps'] = ''
# session stat var to keep track if user has submitted ther gene search parameters
if 'gene_status' not in st.session_state:
    st.session_state['gene_status'] = 'not_run'
# session stat var to keep track if user has submitted ther SNP search parameters
if 'snp_status' not in st.session_state:
    st.session_state['snp_status'] = 'not_run'

if isinstance(st.session_state['main_data'],pd.core.frame.DataFrame):
    main_df = st.session_state['main_data']
else:
    main_df = load_data(st.secrets['simple_sig'])

# genes
main_gene_list = list(main_df['Gene'].unique())
st.session_state['genes_list']  = main_gene_list

# snps
main_snp_list = list(main_df['topRSID'].unique())
st.session_state['snps_list']  = main_snp_list

st.write("Use these interactive tools to search for your gene(s) or SNP(s) of interest against our database.")
with st.container():
    col1, col2= st.columns(2)

    with col1:
        st.title('Gene Search')
        with st.form("Gene_Search"):
            st.subheader('Parameter Selection')

            # user input - genes list
            genes_list = st.text_area('Input a gene or list of genes (seperated by comma):')
            # split list
            genes_list = genes_list.split(',')
            new_genes = []
            for gene in genes_list:
                new_genes.append(gene.strip())

            st.session_state['genes'] = new_genes # add to session state

            # user -  p_val and heidi
            pvalue = st.number_input('P-value threshold', value = 0.05)
            st.session_state['pval'] = pvalue

            heidival = st.number_input('HEIDI p-value threshold', value = 0.01)
            st.session_state['heidi'] = heidival


            # return count df
            count_omic = st.radio('Would you like to return a dataframe that shows how many times a gene shows up in each omic?', ('Yes', 'No'))
            st.session_state['omic_count_gene'] = count_omic
            count_dx = st.radio('Would you like to return a dataframe that shows how many times a gene shows up in each disease?', ('Yes', 'No'))
            st.session_state['dx_count_gene'] = count_dx


            submitted = st.form_submit_button("Search!")
            
            
            if submitted:
                st.session_state['gene_status'] = 'run'

        if st.session_state['gene_status'] == 'run':
            # make sure gene list is correct
            not_genes = []
            for gene in st.session_state['genes']:
                if gene not in st.session_state['genes_list']:
                    not_genes.append(gene)
            
            if len(not_genes) >= 2:
                st.write(f'{", ".join(not_genes)} are not recognized or are not in our dataset. Please check your list and try again.')
            elif len(not_genes) == 1:
                st.write(f'{not_genes[0]} is not recognized or is not in our dataset. Please check your gene and try again.')
            else:
                gene_results_df = main_df[main_df['Gene'].isin(st.session_state['genes'])]
                p_val = st.session_state['pval']
                heidi_val = st.session_state['heidi']
                gene_results_df = gene_results_df.query(f'p_SMR_multi < {p_val} & p_HEIDI > {heidi_val}')
                st.session_state['gene_results_df'] = gene_results_df
                st.subheader('Results dataframe')
                st.dataframe(st.session_state['gene_results_df'])

                st.download_button(label="Download results as CSV", data=convert_df(st.session_state['gene_results_df']), mime='text/csv')

            if st.session_state['omic_count_gene'] == 'Yes' and st.session_state['dx_count_gene'] == 'Yes':
                # omic count
                omic_count_df = pd.crosstab(st.session_state['gene_results_df'].Omic, st.session_state['gene_results_df'].Gene)
                st.session_state['omic_df_gene'] = omic_count_df
                st.subheader('Omic count')
                st.dataframe(st.session_state['omic_df_gene'])
                
                st.download_button(label="Download omic count results as CSV", data=convert_df(st.session_state['omic_df_gene']), mime='text/csv')

                # disease count
                dx_count_df = pd.crosstab(st.session_state['gene_results_df'].Disease, st.session_state['gene_results_df'].Gene)
                st.session_state['dx_df_gene'] = dx_count_df
                st.subheader('Disease count')
                st.dataframe(st.session_state['dx_df_gene'])

                st.download_button(label="Download disease count results as CSV", data=convert_df(st.session_state['dx_df_gene']), mime='text/csv')

            elif st.session_state['omic_count_gene'] == 'Yes' and st.session_state['dx_count_gene'] == 'No':
                # omic count
                omic_count_df = pd.crosstab(st.session_state['gene_results_df'].Omic, st.session_state['gene_results_df'].Gene)
                st.session_state['omic_df_gene'] = omic_count_df
                st.subheader('Omic count')
                st.dataframe(st.session_state['omic_df_gene'])

                st.download_button(label="Download omic count results as CSV", data=convert_df(st.session_state['omic_df_gene']), mime='text/csv')

            elif st.session_state['omic_count_gene'] == 'No' and st.session_state['dx_count_gene'] == 'Yes':
                # disease count
                dx_count_df = pd.crosstab(st.session_state['gene_results_df'].Disease, st.session_state['gene_results_df'].Gene)
                st.session_state['dx_df_gene'] = dx_count_df
                st.subheader('Disease count')
                st.dataframe(st.session_state['dx_df_gene'])

                st.download_button(label="Download disease count results as CSV", data=convert_df(st.session_state['dx_df_gene']), mime='text/csv')
    with col2:
        st.title('SNP Search')
        
        with st.form("SNP_Search"):
            st.subheader('Parameter Selection')

            # user input - snps list
            snps_list = st.text_area('Input a SNP or list of SNPs(dbSNP) (seperated by comma):')
            # split list
            snps_list = snps_list.split(',')
            new_snps = []
            for snp in snps_list:
                new_snps.append(snp.strip())

            st.session_state['snps'] = new_snps # add to session state

            # user -  p_val and heidi
            pvalue = st.number_input('P-value threshold', value = 0.05)
            st.session_state['pval'] = pvalue

            heidival = st.number_input('HEIDI p-value threshold', value = 0.01)
            st.session_state['heidi'] = heidival


        # return count df
            count_omic = st.radio('Would you like to return a dataframe that shows how many times a SNP shows up in each omic?', ('Yes', 'No'))
            st.session_state['omic_count_snp'] = count_omic
            count_dx = st.radio('Would you like to return a dataframe that shows how many times a SNP shows up in each disease?', ('Yes', 'No'))
            st.session_state['dx_count_snp'] = count_dx


            submitted = st.form_submit_button("Search!")
            
            
            if submitted:
                st.session_state['snp_status'] = 'run'

        if st.session_state['snp_status'] == 'run':
            # make sure snp list is correct
            not_snps = []
            for snp in st.session_state['snps']:
                if snp not in st.session_state['snps_list']:
                    not_snps.append(snp)
            
            if len(not_snps) >= 2:
                st.write(f'{", ".join(not_snps)} are not recognized or are not in our dataset. Please check your list and try again.')
            elif len(not_snps) == 1:
                st.write(f'{not_snps[0]} is not recognized or is not in our dataset. Please check and try again.')
            else:
                snp_results_df = main_df[main_df['topRSID'].isin(st.session_state['snps'])]
                p_val = st.session_state['pval']
                heidi_val = st.session_state['heidi']
                snp_results_df = snp_results_df.query(f'p_SMR_multi < {p_val} & p_HEIDI > {heidi_val}')
                st.session_state['snp_results_df'] = snp_results_df
                st.subheader('Results dataframe')
                st.dataframe(st.session_state['snp_results_df'])

                st.download_button(label="Download results as CSV", data=convert_df(st.session_state['snp_results_df']), mime='text/csv')

                if st.session_state['omic_count_snp'] == 'Yes' and st.session_state['dx_count_snp'] == 'Yes':
                    # omic count
                    omic_count_df = pd.crosstab(st.session_state['snp_results_df'].Omic, st.session_state['snp_results_df'].topRSID)
                    st.session_state['omic_df_snp'] = omic_count_df
                    st.subheader('Omic count')
                    st.dataframe(st.session_state['omic_df_snp'])
                    
                    st.download_button(label="Download omic count results as CSV", data=convert_df(st.session_state['omic_df_snp']), mime='text/csv')

                    # disease count
                    dx_count_df = pd.crosstab(st.session_state['snp_results_df'].Disease, st.session_state['snp_results_df'].topRSID)
                    st.session_state['dx_df_snp'] = dx_count_df
                    st.subheader('Disease count')
                    st.dataframe(st.session_state['dx_df_snp'])

                    st.download_button(label="Download disease count results as CSV", data=convert_df(st.session_state['dx_df_snp']), mime='text/csv')

                elif st.session_state['omic_count'] == 'Yes' and st.session_state['dx_count'] == 'No':
                    # omic count
                    omic_count_df = pd.crosstab(st.session_state['snp_results_df'].Omic, st.session_state['snp_results_df'].topRSID)
                    st.session_state['omic_df_snp'] = omic_count_df
                    st.subheader('Omic count')
                    st.dataframe(st.session_state['omic_df_snp'])

                    st.download_button(label="Download omic count results as CSV", data=convert_df(st.session_state['omic_df_snp']), mime='text/csv')

                elif st.session_state['omic_count'] == 'No' and st.session_state['dx_count'] == 'Yes':
                    # disease count
                    dx_count_df = pd.crosstab(st.session_state['snp_results_df'].Disease, st.session_state['snp_results_df'].topRSID)
                    st.session_state['dx_df_snp'] = dx_count_df
                    st.subheader('Disease count')
                    st.dataframe(st.session_state['dx_df_snp'])

                    st.download_button(label="Download disease count results as CSV", data=convert_df(st.session_state['dx_df_snp']), mime='text/csv')