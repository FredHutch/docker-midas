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

@test "Make sure MIDAS is in the PATH" {
  h="$(run_midas.py -h)"

  [[ "$h" =~ "Estimate species abundance and intra-species genomic variation from an individual metagenome" ]]
}

@test "Make sure the run script is in the PATH" {
  h="$(run.py -h)"

  [[ "$h" =~ "Analyze a set of reads with MIDAS" ]]
}