import csv


PROTEIN_MAPPING_STRING = dict()
PROTEIN_MAPPING_UNIPROT = dict()


def prepare_mapping(*args):
    def _download_and_append(aux_file):
        with open(aux_file) as f:
                rows = csv.reader(f, delimiter="\t")
                for row in rows:
                    PROTEIN_MAPPING_STRING[row[1]] = row[0]
                    PROTEIN_MAPPING_UNIPROT[row[0]] = row[1]
        f.close()
    list(map(_download_and_append, args))
