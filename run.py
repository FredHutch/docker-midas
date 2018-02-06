#!/usr/bin/python
"""Wrapper script to run FAMLI on one or more FASTQ files."""

import os
import uuid
import time
import shutil
import logging
import argparse
from lib.midas_helpers import run_midas
from lib.midas_helpers import parse_midas_output
from lib.exec_helpers import get_reference_database
from lib.exec_helpers import return_results
from lib.exec_helpers import exit_and_clean_up
from lib.fastq_helpers import get_reads_from_url
from lib.fastq_helpers import count_fastq_reads


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Analyze a set of reads with MIDAS.
    """)

    parser.add_argument("--input",
                        type=str,
                        help="""Location for input file(s). Comma-separated.
                                (Supported: sra://, s3://, or ftp://).""")
    parser.add_argument("--ref-db",
                        type=str,
                        help="""Folder containing reference database.
                                (Supported: s3://, ftp://, or local path).""")
    parser.add_argument("--output-folder",
                        type=str,
                        help="""Folder to place results.
                                (Supported: s3://, or local path).""")
    parser.add_argument("--threads",
                        type=int,
                        default=16,
                        help="Number of threads to use aligning.")
    parser.add_argument("--temp-folder",
                        type=str,
                        default='/share',
                        help="Folder used for temporary files.")

    args = parser.parse_args()

    # Make a temporary folder for all files to be placed in
    temp_folder = os.path.join(args.temp_folder, str(uuid.uuid4())[:8])
    assert os.path.exists(temp_folder) is False
    os.mkdir(temp_folder)

    # Set up logging
    log_fp = os.path.join(temp_folder, "log.txt")
    logFormatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s [MIDAS] %(message)s'
    )
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    # Write to file
    fileHandler = logging.FileHandler(log_fp)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    # Also write to STDOUT
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Get the reference database
    try:
        db_fp = get_reference_database(
            args.ref_db,
            temp_folder
        )
    except:
        exit_and_clean_up(temp_folder)

    logging.info("Reference database: " + db_fp)

    # Align each of the inputs and calculate the overall abundance
    for input_str in args.input.split(','):
        # Keep track of the time elapsed to process each sample
        start_time = time.time()

        # Make a new temporary folder for this sample
        sample_temp_folder = os.path.join(temp_folder, str(uuid.uuid4())[:8])
        assert os.path.exists(sample_temp_folder) is False
        logging.info(
            "Making temp folder for this sample: {}".format(sample_temp_folder)
        )
        os.mkdir(sample_temp_folder)

        logging.info("Processing input argument: " + input_str)

        # Capture each command in a try statement
        # Get the input reads
        try:
            read_fp = get_reads_from_url(input_str, sample_temp_folder)
        except:
            exit_and_clean_up(temp_folder)

        # Run MIDAS
        try:
            output_folder = run_midas(
                read_fp,               # FASTQ file path
                db_fp,                 # Local path to DB
                sample_temp_folder,           # Folder for results
                threads=args.threads,
            )
        except:
            exit_and_clean_up(temp_folder)

        # Parse the output
        try:
            midas_summary = parse_midas_output(
                output_folder,
                ref_db=db_fp,
            )
        except:
            exit_and_clean_up(temp_folder)

        # Name the output file based on the input file
        # Ultimately adding ".json.gz" to the input file name
        output_prefix = input_str.split("/")[-1]

        # Count the total number of reads
        logging.info("Counting the total number of reads")
        n_reads = count_fastq_reads(read_fp)
        logging.info("Reads in input file: {}".format(n_reads))

        # Read in the logs
        logging.info("Reading in the logs")
        logs = open(log_fp, 'rt').readlines()

        # Wrap up all of the results into a single JSON
        # and write it to the output folder
        output = {
            "input_path": input_str,
            "input": output_prefix,
            "output_folder": args.output_folder,
            "logs": logs,
            "ref_db": db_fp,
            "ref_db_url": args.ref_db,
            "results": midas_summary,
            "total_reads": n_reads,
            "time_elapsed": time.time() - start_time
        }
        return_results(
            output, output_prefix, args.output_folder, sample_temp_folder
        )

        # Delete any files that were created for this sample
        logging.info("Removing temporary folder: " + sample_temp_folder)
        shutil.rmtree(sample_temp_folder)

    # Delete all files created for this analysis
    logging.info("Removing temporary folder: " + temp_folder)
    shutil.rmtree(temp_folder)

    # Stop logging
    logging.info("Done")
    logging.shutdown()
