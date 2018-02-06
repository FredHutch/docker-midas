# Docker - MIDAS

[![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/midas/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/midas)

This repository provides a Docker image for running MIDAS that is compatible with automated analysis on AWS Batch. Specifically, this image includes a wrapper script that:


  1. Downloads reference databases

  2. Downloads input data

  3. Runs MIDAS

  4. Saves the outputs to persistent storage


In order to be compatible with AWS Batch, all of these steps are parameterizable and are run with a single command.


### Wrapper script options

#### --input

Specifies the set of FASTQ reads that will be aligned. Supports files from SRA, S3, or FTP. Use the file prefix to specify the source (`s3://`, `sra://`, or `ftp://`). Note that for SRA, just provide the accession (e.g. `sra://SRR123456`).

#### --ref-db

Path to the MIDAS reference database (folder). Supports `s3://`, or a local path.

#### --output-folder

Folder to place the output in, supporting either `s3://` or a local path. Output files will take the form of `<prefix>.json.gz`, where `<prefix>` is the SRA accession (if specified), or otherwise the prefix of the input file from S3 or ftp. 

#### --threads

Number of threads used by MIDAS during alignment, defaults to 16.

### Output format


```
{
  "input_path": <PATH_TO_INPUT_DATA>,
  "input": <INPUT_DATA_PREFIX>,
  "output_folder": <OUTPUT_FOLDER_PATH>,
  "logs": <ANALYSIS_LOGS>,
  "ref_db": <LOCAL_PATH_TO_REF_DB>,
  "ref_db_url": <URL_FOR_REF_DB>,
  "total_reads": <INT>,
  "time_elapsed": <FLOAT_SECONDS>,
  "results": {
    "species": [
      {
        "species_id": "Clostridium_botulinum_57664",
        "relative_abundance": 0.966368434694,
        "count_reads": 5631,
        "coverage": 95.0686106346
      },
      ...species level data for more species...
    ],
    "genes": [
      {
        "species_id": "Clostridium_sporogenes_58038",
        "marker_coverage": 0,
        "fraction_covered": 0.112485472356,
        "aligned_reads": 98310,
        "covered_genes": 1355,
        "mean_coverage": 6.65663712323,
        "mapped_reads": 49030,
        "pangenome_size": 12046
        "genes": [
          {
            "copy_number": 0,
            "count_reads": 47,
            "coverage": 5.62211614956,
            "gene_id": "1075091.3.peg.1003",
            "annot": {
              "figfam": [
                "FIG00517132"
              ]
            }
          },
          ...more genes...
          ]
        },
        ...gene level data for more species...
      ]
    }
}
```

