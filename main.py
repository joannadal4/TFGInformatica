"""Main module."""
import json

from hmm import get_proteins, split_models
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
                go_functions.add(get_go_functions(protein))

            data[model] = {'proteins': proteins, 'go_functions': go_functions}

    with open(output_file, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
