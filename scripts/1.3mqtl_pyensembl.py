import glob
import pandas as pd
import pyensembl

def gene_rename(df, release = 75):
    
    ensembl = pyensembl.EnsemblRelease(release)
    
    gene_list = []
    for c,p in zip(df['ProbeChr'],df['Probe_bp']):
        # try pulling data using probe chr and bp
        try:
            opt = ensembl.gene_names_at_locus(c,p)
            if isinstance(opt,list):
                if len(opt) == 1:
                    gene_list.append(opt[0])
                elif len(opt) > 1:
                    gene_list.append(','.join(opt))
                else:
                    gene_list.append('novel_or_none')
            else:
                gene_list.append(opt)
        except:
            gene_list.append('none')
            
    df['Gene_pyensembl'] = gene_list
    
    return df


# glob for SMR results and filter for mMeta + mcrae
msmr_files = glob.glob("/../omicSynth/intermediate_results/*.msmr")

# filter for files we care about
mmeta = [x for x in msmr_files if 'mMeta' in x]

mcrae = [x for x in msmr_files if 'mcrae' in x]

# merge all mQTL paths into one list
mqtl_paths = mmeta + mcrae

# read in paths and create central df
mqtl_df = pd.DataFrame()

for path in mqtl_paths:
    tmp = pd.read_csv(path, sep = '\t')
    
    # concat main df and tmp df
    mqtl_df = pd.concat([mqtl_df,tmp])

mqtl_anno = gene_rename(mqtl_df)

mqtl_anno.to_csv('mQTL_anno.csv', index = False, sep = ',')