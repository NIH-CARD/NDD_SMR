#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)
library(foreach)
library(rhdf5)



goi_filename <- 'genes_of_interest.tsv'
loom_obj <- '/data/CARD_AA/users/wellerca/data/adult_human_20221007.loom'
out_filename <- 'goi_percentiles_from_R.tsv'

out_dir <- '/data/CARD_AA/users/wellerca/data/'

# 59480 genes
# 3369219 cells
# I use h5py to read the datasets because loom is stupid

# Load the rhdf5 package
library(rhdf5)

# Open the H5 object
h5_file <- H5Fopen(loom_obj)

# Read a dataset from the H5 object
cellIDs <- h5read(h5_file, "col_attrs/CellID")
gene_Symbols <- h5read(h5_file, "row_attrs/Gene")
gene_ENSEMBL <- h5read(h5_file, "row_attrs/Accession")

chunk_cellIDs <- cellIDs[start_idx:stop_idx]

n_cells <- length(cellIDs)
n_genes <- length(gene_ENSEMBL)


get_TPM <- function(counts) {
    # Divide counts by transcript length
    normcounts <- counts * one_over_tx_lengths

    # Calculate scaling factor,the sum of all normalized counts
    T <- sum(normcounts)

    # TPM is equal to normalized counts * (1e6/T)
    TPM <- as.integer(round(normcounts * (1e6/T)))
    return(TPM)
}





if (! file.exists('tx_lengths.tsv')) {

    # build data.table of ENSEMBL ids from Linnarsson h5
    dat1 <- data.table('ENSEMBL' = gene_ENSEMBL)

    # add row index integers
    dat1[, idx := 1:.N] # for reordering later

    # Calculation gene-specific exon lengths
    library(GenomicFeatures) 

    gtf_filename <- 'gb_pri_annot.gtf'

    # Import GTF into R 
    txdb <- makeTxDbFromGFF(gtf_filename,format="gtf")

    # Build gene-specific exon list
    exons.list.per.gene <- exonsBy(txdb, by='gene')

    # Calculate intron-removed transcript length table
    exonic.gene.sizes <- as.data.frame(sum(width(reduce(exons.list.per.gene))))


    dat2 <- as.data.table(exonic.gene.sizes, keep.rownames=TRUE)
    setnames(dat2, c('ENSEMBL', 'TX_LENGTH'))

    # Merge in transcript length values
    tx_lengths <- merge(dat1, dat2, by='ENSEMBL', all=T)[order(idx)]

    fwrite(tx_lengths, file='tx_lengths.tsv', sep='\t')

} else {
    tx_lengths <- fread('tx_lengths.tsv')
}

# multiply by 1/TX_LENGTH
# (equivalent to divide by TX_LENGTH) but allows us to set
# genes to ignore as 0, so TPM will also be 0
tx_lengths[, const := 1/TX_LENGTH]
tx_lengths[is.na(TX_LENGTH), const := 0]

# Will ignore these 21 features
#     pcDNA3-CFP_951-1700
#                    Cas9
#             pET-mOrange
#        pCS-Cre2_51-1150
# pCS-Cherry-DEST_101-850
#              pCAG-HcRed
#      pCAG-GFP_1751-2500
#               pCAG-EYFP
#     pCAG-DsRed2_101-650
#                  gRNA16
#                  gRNA15
#                  gRNA14
#                  gRNA13
#                  gRNA11
#                    WRPE
#  FUdGW-Tomato_3801-5300
#       piRFP670-N1_1-950
#                    EGFP
#                  gRNA10
#                  gRNA12
#                  gRNA17


one_over_tx_lengths <- tx_lengths$const

chunk_size <- 5000

for(start_idx in seq(1,n_cells,chunk_size)) {
    
    stop_idx <- start_idx + chunk_size - 1
    outfilename <- paste0(out_dir, 'TPM_', start_idx, '_', stop_idx, '.tsv.gz')

    # go to next chunk if file exists
    if(file.exists(outfilename)) {
        next
    }


    print(c(start_idx, stop_idx))

    # chunk <- h5read(h5_file, name='matrix', index=list(1, 1 : n_genes))
    chunk <- h5read(h5_file, name='matrix', index=list(start_idx:stop_idx, NULL))

    used_ids <- as.character(cellIDs[start_idx:stop_idx])

    chunk_TPM <- data.table('cell_ID'=used_ids)
    chunk_TPM <- cbind(chunk_TPM, as.data.table(t(apply(chunk, 1, get_TPM))))

    fwrite(chunk_TPM, file=outfilename, sep='\t')

}



h5closeAll()

quit(status=0)

