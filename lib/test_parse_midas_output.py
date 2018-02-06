#!/usr/bin/python
"""Test the function to parse a set of inputs from MIDAS."""

import json
from midas_helpers import parse_midas_output

out = parse_midas_output(
    "/usr/midas/tests/example_output",
    ref_db="/usr/midas/tests/example_output/ref_db"
)

assert "genes" in out
assert "species" in out

assert len(out["species"]) == 5
assert json.dumps(out["species"]) == json.dumps([
    {
        "species_id": "Salmonella_enterica_58156",
        "count_reads": int(147),
        "coverage": float(3.13765227021),
        "relative_abundance": float(0.815123262907)
        },

    {
        "species_id": "Salmonella_enterica_58266",
        "count_reads": int(27),
        "coverage": float(0.558183718058),
        "relative_abundance": float(0.145009228041)
        },

    {
        "species_id": "Salmonella_enterica_53987",
        "count_reads": int(7),
        "coverage": float(0.139110604333),
        "relative_abundance": float(0.0361392149109)
        },

    {
        "species_id": "Klebsiella_oxytoca_56762",
        "count_reads": int(1),
        "coverage": float(0.00539967216276),
        "relative_abundance": float(0.00140276806124)
        },

    {
        "species_id": "Xanthomonas_campestris_57487",
        "count_reads": int(1),
        "coverage": float(0.00895164267257),
        "relative_abundance": float(0.00232552607978)}
])

assert len(out["genes"]) == 1
assert out["genes"][0]["species_id"] == "Salmonella_enterica_58156"
assert len(out["genes"][0]["genes"]) == 22927

assert out["genes"][0]["genes"][0]["gene_id"] == "1003185.3.peg.1459"
assert out["genes"][0]["genes"][0]["annot"] == {"figfam": ["FIG00626808"]}

print("Passed all tests")
