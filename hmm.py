import re
import subprocess
import tempfile
from typing import List

from config import UNIPROT_DATABASE
from constants import REGEX_NAME


def split_models(models_file: str) -> List[str]:
    """Get one model files, split in one file per model and returns the model names."""
    models = []
    with open(models_file) as f:
        model_name = None
        model_lines = []
        for line in f:
            model_lines.append(line)
            if line == "//\n":
                with open(f"data/models/{model_name}.hmm") as f_model:
                    f_model.writelines(model_lines)
                    model_lines = []
                    models.append(model_name)
            if line.startswith("NAME"):
                model_name = re.findall(REGEX_NAME, line)[0]

    return models


def get_proteins(model: str) -> List[str]:
    """Compute hmmsearch and returns the list of matching proteins."""
    output_file = tempfile.TemporaryFile()
    subprocess.call(["hmmsearch", "--tblout", output_file.name, f"data/models/{model}.hmm", UNIPROT_DATABASE])
    proteins = get_proteins_from_hmmsearch_file(output_file.readlines())
    output_file.close()
    return proteins


def get_proteins_from_hmmsearch_file(lines: List[str]):
    raise NotImplementedError
