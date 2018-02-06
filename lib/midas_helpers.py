#!/usr/bin/python

import os
import gzip
import logging
from collections import defaultdict
from exec_helpers import run_cmds


def parse_table_to_json(fp, sep="\t", nrows=0):
    """Parse a TSV into JSON format."""
    output = []

    if fp.endswith(".gz"):
        with gzip.open(fp, "rt") as f:
            header = f.readline()
            header = header.rstrip("\n").split(sep)

        f = gzip.open(fp, "rt")
    else:
        with open(fp, "rt") as f:
            header = f.readline()
            header = header.rstrip("\n").split(sep)

        f = open(fp, "rt")

    for ix, values in enumerate(f):
        # Skip the header line
        if ix == 0:
            continue
        if nrows > 0 and ix == nrows:
            break
        # Parse the line
        values = values.rstrip("\n").split(sep)
        # Add to the output
        if len(values) == len(header):
            output.append(set_variable_type(header, values))

    f.close()

    return output


def set_variable_type(
    header,
    values,
    types={
        "species_id": str,
        "relative_abundance": float,
        "count_reads": int,
        "coverage": float,
        "copy_number": float,
        "pangenome_size": int,
        "covered_genes": int,
        "fraction_covered": float,
        "mean_coverage": float,
        "marker_coverage": float,
        "aligned_reads": int,
        "mapped_reads": int,
        "covered_bases": int,
        "genome_length": int,
        "count_a": int,
        "count_t": int,
        "count_c": int,
        "count_g": int,
        "depth": int,
        "ref_pos": int,
    }
):
    """Make a dict, but set the variable type as appropriate."""
    return {
        k: types.get(k, str)(v)
        for k, v in zip(header, values)
    }


def run_midas(
    read_fp,               # FASTQ file path
    db_fp,                 # Local path to DB
    temp_folder,           # Folder for results
    threads=1
):
    logging.info("Running MIDAS on {}".format(read_fp))
    logging.info("Reference database: {}".format(db_fp))
    logging.info("Threads: {}".format(threads))

    assert os.path.exists(read_fp)

    # Make the output folder in the temp folder, based on the read name
    output_folder = os.path.join(
        temp_folder,
        "{}.midas".format(read_fp.split('/')[-1])
    )

    # Run the species abundance summary
    logging.info("Running species summary")
    run_cmds([
        "run_midas.py",
        "species",
        output_folder,
        "-1", read_fp,
        "-t", str(threads),
        "--remove_temp",
        "-d", db_fp
    ])
    assert os.path.exists(
        os.path.join(output_folder, "species")
    )

    # Run the gene abundance summary
    logging.info("Running gene summary")
    run_cmds([
        "run_midas.py",
        "genes",
        output_folder,
        "-1", read_fp,
        "-t", str(threads),
        "--remove_temp",
        "-d", db_fp
    ])
    assert os.path.exists(
        os.path.join(output_folder, "genes")
    )

    logging.info("Done running MIDAS")

    return output_folder


def annotate_gene_results(gene_results, species_name, ref_db):
    """Annotate a set of gene results."""
    pan_genome_file = os.path.join(
        ref_db, "pan_genomes", species_name, "centroid_functions.txt.gz"
    )

    annotations = {
        d["gene_id"]: defaultdict(list)
        for d in gene_results
    }

    if os.path.exists(pan_genome_file):
        with gzip.open(pan_genome_file) as f:
            for line in f:
                line = line.rstrip("\n").split("\t")
                if len(line) != 3:
                    continue
                if line[0] in annotations:
                    annotations[line[0]][line[2]].append(line[1])

    for d in gene_results:
        d["annot"] = annotations[d["gene_id"]]

    return gene_results


def parse_midas_output(output_folder, ref_db=None):
    """Parse the output from MIDAS."""

    # Make sure the input exists
    assert os.path.exists(output_folder)

    output = {}

    # Parse the species information
    logging.info("Parsing the species abundance information")
    species_fp = os.path.join(output_folder, "species", "species_profile.txt")
    assert os.path.exists(species_fp)
    output["species"] = parse_table_to_json(species_fp)

    # Filter down to the species with >0 reads
    output["species"] = [d for d in output["species"] if d["count_reads"] > 0]

    # Read in the genes results, if present
    genes_folder = os.path.join(output_folder, "genes")
    if os.path.exists(genes_folder):

        output["genes"] = parse_table_to_json(
            os.path.join(genes_folder, "summary.txt")
        )

        for species in output["genes"]:
            species_details_fp = os.path.join(
                genes_folder,
                "output",
                species["species_id"] + ".genes.gz"
            )

            if os.path.exists(species_details_fp):
                logging.info(
                    "Parsing gene output for {}".format(species["species_id"])
                )

                # Read in the genes that were detected
                gene_results = parse_table_to_json(
                    os.path.join(species_details_fp)
                )

                # Filter to the genes with >0 count_reads
                gene_results = [
                    d
                    for d in gene_results
                    if d["count_reads"] > 0
                ]

                # Annotate the gene results with the gene functions
                if ref_db is not None:
                    logging.info("Adding gene annotations")
                    gene_results = annotate_gene_results(
                        gene_results,
                        species["species_id"],
                        ref_db
                    )

                species["genes"] = gene_results
    else:
        logging.info("No gene abundance information found")

    return output
