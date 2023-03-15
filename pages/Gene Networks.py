import streamlit as st

def network_link(genes):
    base_url = 'https://genemania.org/search/homo-sapiens/'
    options = ''
    for gene in genes:
        options += f'/{gene}'
    final_url = base_url + options
    
    return final_url

# session state variables for  gene dataframe
if 'genes_list' not in st.session_state: # user provided genes
    st.session_state['genes_list'] = None
if 'gene_results_run' not in st.session_state:
    st.session_state['gene_results_run'] = None

st.title('Gene Network')
st.write('Provide a list of genes to build a network from GeneMANIA and receive a link to the network.')

# user input - genes list
genes_list = st.text_area('Input a list of genes (seperated by comma):')
# split list
genes_list = genes_list.split(',')
new_genes = []
for gene in genes_list:
    new_genes.append(gene.strip())

st.session_state['genes_list'] = new_genes # add to session state

gene_results_run = st.button('Submit')
if gene_results_run:
    st.session_state['gene_results_run'] = 'run'

if st.session_state['gene_results_run'] == 'run':
    link = network_link(st.session_state['genes_list'])

    st.markdown(f"[Click here]({link}) to be redirected to your network!")