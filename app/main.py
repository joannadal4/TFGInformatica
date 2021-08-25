"""Main module."""
from hmm import get_proteins, split_models, save_protein
from function import get_go_functions
from interaction import get_interactions, save_interaction
from mapping import prepare_mapping, PROTEIN_MAPPING_STRING, PROTEIN_MAPPING_UNIPROT
from config import VIRUS_MAPPING_FILE, MODELS_FILE, HOST_MAPPING_FILE, INTERACTIONS_FILE


def main(models_file: str) -> None:
    """Split hmm models and get them proteins and go functions as well as their interactions with host proteins."""

    models = split_models(models_file)
    prepare_mapping(VIRUS_MAPPING_FILE, HOST_MAPPING_FILE)
    interactions = get_interactions(INTERACTIONS_FILE)
    for model in models:
        proteins = get_proteins(model)
        if not proteins:
            continue
        host_proteins= []
        for protein in proteins:
            get_go_functions(protein)
            virus_string_code = PROTEIN_MAPPING_STRING.get(protein)
            if virus_string_code is None:
                continue
            host_proteins = interactions.get(virus_string_code)
            if not host_proteins:
                continue
            for host_protein in host_proteins:
                host_uniprot_code = PROTEIN_MAPPING_UNIPROT.get(host_protein)
                if host_uniprot_code is not None:
                    save_protein(host_uniprot_code)
                    get_go_functions(host_uniprot_code)
                    save_interaction(protein, host_uniprot_code)

if __name__ == "__main__":
    main(MODELS_FILE)
