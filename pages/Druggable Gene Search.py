import streamlit as st
import pandas as pd

@st.cache
def load_data(url, sheet_name="Sheet"):
    sh = st.session_state['client_auth'].open_by_url(url)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    return df

def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(index = False)

def drug_search(genes_list, df):
    
    # list of thera genes
    thera_genes = list(df['gene_name'])
    # check gene list to see if user genes are in druggable genome
    no_gene = []
    yes_gene = []
    for gene in genes_list:
        if gene not in thera_genes:
            no_gene.append(gene)
        else:
            yes_gene.append(gene)

    # sort lists for alphabetical order - just a little extra cleaning up
    no_gene.sort() 
    yes_gene.sort()
           
    # let user know if any of their genes are not drug targets     
    if len(no_gene) == 1:
        no_result = f'{no_gene[0]} does not have any known therapeutic targets or interactions. Please check your target gene for spelling/formatting and try again.'
    elif len(no_gene) > 1 and len(no_gene) < 3:
        no_result = f'{" and  ".join(no_gene)} do not have any known therapeutics targets or interactions. Please check your target genes for spelling/formatting and try again.'
    elif len(no_gene) > 2:
        no_result = f'{", ".join(no_gene[:-1])}, and {no_gene[-1]} do not have any known therapeutics targets or interactions. Please check your target genes for spelling/formatting and try again.'
    else:
        no_result = None
    
    if yes_gene:
        # return any known drug targets
        results = df.query("gene_name == @yes_gene")
        res_stat = True
        print(f'{", ".join(yes_gene)} are known drug targets!')
    else:
        results = None
        res_stat = False
        
    return results, no_result, res_stat


# session state variables for gene dataframe
if 'genes_list' not in st.session_state: # user provided genes
    st.session_state['genes_list'] = None
if 'gene_results_df' not in st.session_state:
    st.session_state['gene_results_df'] = None
if 'gene_results_run' not in st.session_state:
    st.session_state['gene_results_run'] = None

# session state variables for druggable gene dataframe
if 'drugdf' not in st.session_state:
    st.session_state['drugdf'] = None

# ss var for genes in db
if 'thera_genes' not in st.session_state:
    st.session_state['thera_genes'] = None

## ss var for dropdown gene list options
if 'filter_submit_genes' not in st.session_state:
    st.session_state['filter_submit_genes'] = None


## ss var for dataframe produced from user selecting drug db genes to return
if 'pre_res_df' not in st.session_state:
    st.session_state['pre_res_df'] = None

# load in druggable genome list
drug_df = load_data(st.secrets['drug_db'])
st.session_state['drugdf'] = drug_df

# get list of genes in db
thera_genes = list(st.session_state['drugdf']['gene_name'])

# set ss variable for drug db genes
st.session_state['thera_genes'] = thera_genes

# container for user to search from available genes in drug db
with st.container():
    with st.form('Select Druggable Genes'):
        st.title('Druggable Gene Search')

        st.write('Select genes availble in our aggregated database to obtain more information.')

        # create drop down for user input
        gene_options = st.multiselect('Select from available genes', st.session_state['thera_genes'])

        submitted = st.form_submit_button("Retrieve Druggable Gene Data")

        if submitted:
            # update session state var
            st.session_state['filter_submit_genes'] = 'run'
            preselect_df = st.session_state['drugdf']
            preselect_df = preselect_df.query('gene_name == @gene_options')
            st.session_state['pre_res_df'] = preselect_df

            # display results dataframe
            st.dataframe(st.session_state['pre_res_df'])

    if st.session_state['filter_submit_genes'] == 'run':
        # allow user to download results
        st.download_button(label="Download results as CSV", data=convert_df(st.session_state['pre_res_df']), mime='text/csv')

    

with st.container():
    st.title('Custom Druggable Gene Search')
    st.write('Provide a gene or list of genes to search against our aggregated therapeutic target database.')

    # user input - genes list
    genes_list = st.text_area('Input a gene or list of genes (seperated by comma):')
    # split list
    genes_list = genes_list.split(',')
    new_genes = []
    for gene in genes_list:
        new_genes.append(gene.strip())

    st.session_state['genes_list'] = new_genes # add to session state

    # user submits list
    search_run = st.button('Submit')

    if search_run:
        st.session_state['gene_results_run'] = 'run'

    if st.session_state['gene_results_run'] == 'run':
        gene_results, no_gene, thera_status = drug_search(st.session_state['genes_list'], st.session_state['drugdf'])

        if no_gene != None:
            st.write(no_gene)

            st.session_state['gene_results_df'] = gene_results
        else:
            st.session_state['gene_results_df'] = gene_results

        if thera_status == True:
            st.write('**Druggable Targets Results**')
            # display results dataframe
            st.dataframe(st.session_state['gene_results_df'])

            # allow user to download results
            st.download_button(label="Download results as CSV", data=convert_df(st.session_state['gene_results_df']), mime='text/csv')