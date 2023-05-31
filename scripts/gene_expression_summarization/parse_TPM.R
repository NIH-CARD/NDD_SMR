#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)
library(foreach)

if (file.exists('session.Rdata')) {
    load('session.Rdata')
} else {
    loom_obj <- '/data/CARD_AA/users/wellerca/data/adult_human_20221007.loom'
    data_dir <- '/data/CARD_AA/users/wellerca/data/'

    library(rhdf5)                  # Load the rhdf5 package
    h5_file <- H5Fopen(loom_obj)    # Open the H5 object

    # Read the dataset from the H5 object
    cellIDs <- h5read(h5_file, "col_attrs/CellID")
    gene_Symbols <- h5read(h5_file, "row_attrs/Gene")
    gene_ENSEMBL <- h5read(h5_file, "row_attrs/Accession")

    h5closeAll()
    rm(h5_file)

    goi <- readLines('goi.txt')

    file_list <- list.files(data_dir, pattern="TPM_.*.tsv.gz", full.names=TRUE)
    save(list=ls(), file='session.Rdata')
}

# get batch number from auto-set SLURM variable
N <- as.numeric(Sys.getenv('SLURM_ARRAY_TASK_ID'))
cat(paste0('Job Array #', N, '\n'))

# set input to file corresponding to Nth batch
in_filename <- file_list[N]
in_basename <- basename(in_filename)


dat <- fread(in_filename)       # Import TPM data for batch
cell_ids <- dat[['cell_ID']]    # Save cell ID vector for later
dat[, 'cell_ID' := NULL]        # Remove (such that only TPM remain)
dat <- as.matrix(dat)           # Convert to matrix for iteration

# Extract indices from file name
start_idx <- as.numeric(strsplit(in_basename, split='_|\\.')[[1]][2])
stop_idx <- as.numeric(strsplit(in_basename, split='_|\\.')[[1]][3])


out_filename <- paste0(data_dir, 'pct_', start_idx, '-', stop_idx, '.tsv')
cat(paste0('output: ',out_filename, '\n'))

indices_of_interest <- match(goi, gene_Symbols)

# Error checking just in case--this should not happen
if( length(indices_of_interest) != length(goi) ) {
    cat("ERROR: Genes of interest exist multiple times within gene IDs!\n")
    quit(status=1)
}

# Iterate over all cells in batch
o <- foreach(i=1:nrow(dat)) %do% {
    V <- dat[i,]
    values_of_interest <- (V[indices_of_interest] - 1)
    cdf <- ecdf(V)
    percentiles <- floor(100*cdf(values_of_interest))
    return(percentiles)
}

# Format output
ids <- data.table('cell_ID'=cell_ids)
o <- as.data.table(do.call(rbind, o))
setnames(o, goi)
o <- cbind(ids, o)

# Write output
fwrite(o, file=out_filename, sep='\t')

cat("Ran to completion\n")
quit(status=0)

