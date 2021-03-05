"""Main module."""
import json
from argparse import ArgumentParser
from hmm import get_proteins, split_models
from os import rmdir
from uniprot import get_go_functions


def main(models_file: str, output_file: str) -> None:
    """Split hmm models and get it's proteins and go functions."""
    models = split_models(models_file)
    data = {}
    for model in models:
        proteins = get_proteins(model)
        if proteins:
            go_functions = []
            for protein in proteins:
                go_functions.append(get_go_functions(protein))

            data[model] = {'proteins': proteins, 'go_functions': go_functions}

    """folder_data_txt_path = "data/models_txt"
    rmdir(folder_data_txt_path)"""

    with open(output_file, 'w') as f:
        json.dump(data, f)
    f.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("models_file", type=str, help="Models file to read")
    parser.add_argument("output_file", type=str, help="Out file json format")
    args = parser.parse_args()
    main(args.models_file, args.output_file)
