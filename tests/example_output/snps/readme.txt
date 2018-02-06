
Description of output files and file formats from 'run_midas.py snps'

Output files
############
output
  directory of per-species output files
  files are tab-delimited, gzip-compressed, with header
  naming convention of each file is: {SPECIES_ID}.snps.gz
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
output/{SPECIES_ID}.snps.gz
  ref_id: id of reference scaffold/contig/genome
  ref_pos: position in ref_id (1-indexed)
  ref_allele: reference nucleotide
  depth: number of mapped reads
  count_a: count of A allele
  count_c: count of C allele
  count_g: count of G allele
  count_t: count of T allele

summary.txt
  species_id: species id
  genome_length: number of base pairs in representative genome
  covered_bases: number of reference sites with at least 1 mapped read
  fraction_covered: proportion of reference sites with at least 1 mapped read
  mean_coverage: average read-depth across reference sites with at least 1 mapped read
  aligned_reads: number of aligned reads BEFORE quality filtering
  mapped_reads: number of aligned reads AFTER quality filtering
  
Additional information for each species can be found in the reference database:
 /share/midas_db_v1.2/rep_genomes
