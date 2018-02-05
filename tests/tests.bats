#!/usr/bin/env bats

@test "SRA Toolkit v2.8.2" {
  v="$(fastq-dump --version)"
  [[ "$v" =~ "2.8.2" ]]
}


@test "AWS CLI v1.11.146" {
  v="$(aws --version 2>&1)"
  [[ "$v" =~ "1.11.146" ]]
}


@test "Curl v7.47.0" {
  v="$(curl --version)"
  [[ "$v" =~ "7.47.0" ]]
}

@test "Samtools v1.4" {
  v="$(samtools --version)"

  [[ "$v" =~ "samtools 1.4" ]]
}

@test "Bowtie2 2.3.2" {
  v="$(bowtie2 --version)"

  [[ "$v" =~ "bowtie2-align-s version 2.3.2" ]]
}

@test "Make sure MIDAS is in the PATH" {
  h="$(cd /usr/midas/MIDAS-1.3.2/test && run_midas.py -h)"

  [[ "$h" =~ "Estimate species abundance and intra-species genomic variation from an individual metagenome" ]]
}

@test "Make sure the run script is in the PATH" {
  h="$(run.py -h)"

  [[ "$h" =~ "Analyze a set of reads with MIDAS" ]]
}