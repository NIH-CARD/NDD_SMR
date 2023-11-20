import streamlit as st
from PIL import Image

st.title('OmicSynth')

st.write('This tool aims to provide users with the ability to navigate through the SMR Analysis results for our manuscript. Below we provide additional information on data used.')
st.write("")
with st.expander("**GWAS summary statistics information**"):
    st.write("""
    1. AD - [Bellenguez 2022](https://www.nature.com/articles/s41588-022-01024-z)
    2. ALS - [Nicolas 2019](https://pubmed.ncbi.nlm.nih.gov/29566793/)
    3. FTLD - [Pottier 2019](https://link.springer.com/article/10.1007/s00401-019-01962-9)
    4. LBD - [Chia 2021](https://www.nature.com/articles/s41588-021-00785-3)
    5. PD - [Nalls 2019](https://pubmed.ncbi.nlm.nih.gov/31701892/)
    6. PSP - [Hoglinger 2011](https://pubmed.ncbi.nlm.nih.gov/21685912/)""")

with st.expander("**-Omic Details**"):
    st.write("Omic Data Sources for limited data sets available in SMR ready format [here](https://yanglab.westlake.edu.cn/software/smr/#DataResource)")
    col1, col2= st.columns(2)
    with col1:
        st.subheader("""**eQTLs**""")
        tgtex, tmeta, tothereqtl = st.tabs(["GTEx", "MetaBrain", "Other Sources"])
        with tgtex:
            tab1, tab2, tab3 = st.tabs(["Brain", "Other Tissues", "Data Access"])
            with tab1:
                st.write(""" 
                - Amygdala
                - Anterior Cingulate Cortex BA24
                - Caudate Basal Ganglia
                - Cerebellum
                - Cerebellar Hemisphere
                - Cortex
                - Frontal Cortex BA9
                - Hippocampus
                - Hypothalamus
                - Nucleus Accumbens Basal Ganglia
                - Putamen Basal Ganglia
                - Spinal Cord
                """)
            with tab2:
                st.write("""
                - Liver
                - Skeletal Muscle
                - Tibial Nerve
                - Whole Blood
                """)
            with tab3:
                st.write("""
                1. [Original Source](https://www.gtexportal.org/home/datasets) 
 2. [SMR formatted and HG19/GR37 source](https://yanglab.westlake.edu.cn/software/smr/#eQTLsummarydata)""")
        with tmeta:
            st.write(""" 
        - Amygdala
        - Anterior Cingulate Cortex BA24
        - Basal Ganglia
        - Cerebellum
        - Cortex
        - Hippocampus
        - Spinal Cord
        """)
            st.write("[MetaBrain Data Access](https://www.metabrain.nl/index.html)")
        with tothereqtl:
            st.write("""
            - [eQTLgen](https://www.eqtlgen.org/)
            - [Multi-ancestry (Zheng 2022)](https://hoffmg01.hpc.mssm.edu/brema/)
            - [SMR Formatted](https://yanglab.westlake.edu.cn/software/smr/#eQTLsummarydata)
                - BrainMeta v1 (Whole Brain)
                - PsychENCODE
            """)
    with col2:
        st.subheader("Other *-omics")
        tmqtl,tpqtl,tca = st.tabs(['mQTLs', 'pQTLs', 'caQTL'])
        with tmqtl:
            st.write('mQTL data available in SMR ready format [here](https://yanglab.westlake.edu.cn/software/smr/#mQTLsummarydata)')
            st.write('''
            1. Brain-mMeta
            2. Whole Blood (McRae 2018)
            ''')
        with tpqtl:
            
            st.write('''pQTL data is available for access [here](https://www.niagads.org/datasets/ng00102). 
            Summary statistics data are freely available without requiring NIAGADS access by emailing niagads@pennmedicine.upenn.edu 
            to set up a FTP transfer of the data ''')
            st.write('''
            1. Cerebrospinal Fluid (CSF)
            2. Blood Plasma
            3. Brain''')
        with tca:
            st.write('Data is available in SMR ready format [here](https://yanglab.westlake.edu.cn/software/smr/#caQTLsummarydata)')
            st.write('- Bryois 2018 - Prefrontal cortex chromatin peaks')
            
with st.expander("**Additional Data**"):
    st.write("Reference Panel: [1000 Genomes Phase 3](https://www.internationalgenome.org/data-portal/data-collection/phase-3)")
    st.write("Therapeutic gene targets list: [Finan et al., 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6321762/) and [Drug Gene Interaction Database - DGIdb](https://www.dgidb.org/)")
    st.write("Github with code: [NIH CARD Github](https://github.com/NIH-CARD/NDD_SMR)")
    st.write("Single Cell Data [Siletti et al (2022)](https://github.com/linnarsson-lab/adult-human-brain)")
with st.expander("**Data Downloads**"):
    st.subheader('Download SMR results data')
    st.write('Data is available on [Google Drive](https://drive.google.com/drive/u/0/folders/16lB70BgRKA8yjXuAdW3OntHIrR8gqADO)')
    st.subheader('Druggable Genes Data')
    st.write('Download druggable genes and drugs data [here](https://drive.google.com/file/d/1H1tc01B2FHpCie1svvKSIt8nEa_Q7D0j/view?usp=drive_link)')

        
st.write("Data curated by NIH CARD and Data Tecnica International.")

# add CARD logo
card_img = Image.open('img/CARD-logo-white-print.png')
dti_img = Image.open('img/dti_img.jpeg')

st.sidebar.image(card_img)
st.sidebar.image(dti_img)