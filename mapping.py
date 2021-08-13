import csv


PROTEIN_MAPPING_STRING = dict()
PROTEIN_MAPPING_UNIPROT = dict()


def prepare_mapping(*args):
    """Prepare a dictionary in order to given a UniProt code protein get a String code protein"""
    def _download_and_append(aux_file):
        with open(aux_file) as f:
                rows = csv.reader(f, delimiter="\t")
                for row in rows:
                    PROTEIN_MAPPING_STRING[row[1]] = row[0]
                    PROTEIN_MAPPING_UNIPROT[row[0]] = row[1]
    list(map(_download_and_append, args))
