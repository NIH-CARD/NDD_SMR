import streamlit as st

st.title('OmicSynth')

st.write('This tool aims to provide users with the ability to navigate through the SMR Analysis results for our manuscript.')
st.write("All data used is publicly available")
st.write("GWAS summary statistics used include:")
st.write("""
1. AD - [Bellenguez 2022](https://www.nature.com/articles/s41588-022-01024-z)
2. ALS - [Nicolas 2019](https://pubmed.ncbi.nlm.nih.gov/29566793/)
3. FTLD - [Pottier 2019](https://link.springer.com/article/10.1007/s00401-019-01962-9)
4. LBD - [Chia 2021]('https://www.nature.com/articles/s41588-021-00785-3)
5. PD - [Nalls 2019](https://pubmed.ncbi.nlm.nih.gov/31701892/')
6. PSP - [Hoglinger 2011](https://pubmed.ncbi.nlm.nih.gov/21685912/""")
st.write("Reference Panel: 1000 Genomes")
st.write("Omic Data Sources: Available in SMR ready format [here](https://yanglab.westlake.edu.cn/software/smr/#DataResource)")
st.write("""1. GTEx v8 eQTL data <br> - [Original Source](https://www.gtexportal.org/home/datasets) <br> - [SMR formatted and HG19/GR37 source](https://yanglab.westlake.edu.cn/software/smr/#DataResource)""")
st.write("Therapeutic gene targets list: [Finan et al., 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6321762/) and [Drug Gene Interaction Database - DGIdb](https://www.dgidb.org/)")
st.write("Data curated by NIH CARD and Data Tecnica International.")
st.write("Github with code: [NIH CARD Github] (https://github.com/NIH-CARD/NDD_SMR)")
