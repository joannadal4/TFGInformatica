"""Main module."""
import json
from argparse import ArgumentParser
from hmm import get_proteins, split_models
from uniprot import get_go_functions


#from stringViruses import get_proteins_hosts



def main(models_file: str) -> None: #, output_file: str) -> None:
    """Split hmm models and get it's proteins and go functions."""
    models = split_models(models_file)

    """
        from interaction import copy_mapping_virus_from_csv_to_dictionary
        mapping_virus_file = "protein_aliases_virus.txt"
        mapping_virus_dictionary = copy_mapping_virus_from_csv_to_dictionary(mapping_virus_file: str)

        from interaction import copy_mapping_host_from_tsv_to_dictionary
        mapping_host_file = "protein_aliases_host.tsv"
        mapping_host_dictionary = copy_mapping_host_from_tsv_to_dictionary(mapping_host_file: str)

        from interaction import copy_interactions_from_csv_to_dictionary
        interactions_file = "interactions.txt"
        interactions_dictionary = copy_interactions_from_csv_to_dictionary(interactions_file: str)

    """

    for model in models:
        proteins = get_proteins(model)
        if proteins:
            go_functions = []
            #host_proteins= []
            for protein in proteins:
                go_functions.append(get_go_functions(protein))  #Podem eliminar go_functions?
                #get_go_functions(protein)
"""
                from interaction import get_host_proteins
                from interaction import save_interactions
                from hmm import save_protein

                host_proteins = get_host_proteins(protein, interactionsDictionary)

                for host_protein in host_proteins:
                    save_protein(host_protein)
                    get_go_functions(host_protein)

                save_interactions(protein, host_proteins)
"""

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("models_file", type=str, help="Models file to read")
    #parser.add_argument("output_file", type=str, help="Out file json format")
    args = parser.parse_args()

    main(args.models_file) #, args.output_file)
