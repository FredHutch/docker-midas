
Description of output files and file formats from 'run_midas.py genes'

Output files
############
output
  directory of per-species output files
  files are tab-delimited, gzip-compressed, with header
  naming convention of each file is: {SPECIES_ID}.genes.gz
species.txt
  list of species_ids included in local database
summary.txt
  tab-delimited with header
  summarizes alignment results per-species
log.txt
  log file containing parameters used
temp
  directory of intermediate files
  run with `--remove_temp` to remove these files

Output formats
############
output/{SPECIES_ID}.genes.gz
  gene_id: id of non-redundant gene used for read mapping; 'peg' and 'rna' indicate coding & RNA genes respectively
  count_reads: number of aligned reads to gene_id after quality filtering
  coverage: average read-depth of gene_id based on aligned reads (# aligned bp / gene length in bp)
  copy_number: estimated copy-number of gene_id based on aligned reads (coverage of gene_id / median coverage of 15 universal single copy genes)

summary.txt
  species_id: species id
  pangenome_size: number of non-redundant genes in reference pan-genome
  covered_genes: number of genes with at least 1 mapped read
  fraction_covered: proportion of genes with at least 1 mapped read
  mean_coverage: average read-depth across genes with at least 1 mapped read
  marker_coverage: median read-depth across 15 universal single copy genes
  aligned_reads: number of aligned reads BEFORE quality filtering
  mapped_reads: number of aligned reads AFTER quality filtering

Additional information for each species can be found in the reference database:
 /share/midas_db_v1.2/pan_genomes
