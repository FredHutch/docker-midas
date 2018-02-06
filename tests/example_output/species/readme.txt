
Description of output files and file formats from 'run_midas.py species'

Output files
############
species_profile.txt
  tab-delimited with header
  each line contains the abundance values for 1 species (5,952 total species)
  sorted by decreasing relative abundance
log.txt
  log file containing parameters used
temp
  directory of intermediate files
  run with `--remove_temp` to remove these files

Output formats
############
species_profile.txt
  species_id: species identifier
  count_reads: number of reads mapped to marker genes
  coverage: estimated genome-coverage (i.e. read-depth) of species in metagenome
  relative_abundance: estimated relative abundance of species in metagenome

Additional information for each species can be found in the reference database:
 /share/midas_db_v1.2/marker_genes
