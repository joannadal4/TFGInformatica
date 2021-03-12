"""Main module."""
import json
from argparse import ArgumentParser
from hmm import get_proteins, split_models
from uniprot import get_go_functions
#from stringViruses import get_proteins_hosts

def main(models_file: str, output_file: str) -> None:
    """Split hmm models and get it's proteins and go functions."""
    models = split_models(models_file)
    data = {}
    for model in models:
        proteins = get_proteins(model)
        if proteins:
            go_functions = []
            codes = []
            for protein in proteins:
                go_functions.append(get_go_functions(protein))
                """
                1- code = get_name_specie(protein)
                2- codes.append(code)
                3- data[model] = {'proteins': proteins, 'go_functions': go_functions, 'codes': codes}
                """

            data[model] = {'proteins': proteins, 'go_functions': go_functions}
    """
    1- for model in data[model]
    2- for protein in model
    3- if code != null
    4- Take the protein and her code and call get_proteins_host(protein: str, code: str) -> List[str] in stringViruses.py
    5- The List return contains the proteins from hosts which interact with the protein from virus.
    6- for protein_host in list
    7- go_functions_host.append(get_go_functions(protein))
    8- data[protein_host] = {'go_functions_host': go_functions_host}
    9- data[protein] = {'proteins_host': data[protein_host]}
    10- data[model] = {'proteins': data[protein], 'go_functions': go_functions}
    """


    with open(output_file, 'w') as f:
        json.dump(data, f)
    f.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("models_file", type=str, help="Models file to read")
    parser.add_argument("output_file", type=str, help="Out file json format")
    args = parser.parse_args()
    main(args.models_file, args.output_file)
