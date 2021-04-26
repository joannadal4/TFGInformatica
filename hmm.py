import re
import subprocess, shlex
import tempfile
import os
from os import mkdir
from typing import List

from config import UNIPROT_DATABASE
from constant import REGEX_NAME, REGEX_PROTEIN
import psycopg2
from psycopg2 import Error
from psycopg2 import sql



user = "postgres"
password = "postgres"
db_name = "modelvpf"
db_port = "1234"
db_host = "127.0.0.1"


def split_models(models_file: str) -> List[str]:
    """Get one model files, split in one file per model and returns the model names."""
    models = []
    folder_models_path = "data/models_hmm"
    if not os.path.exists("data"):
        mkdir("data")
    if not os.path.exists(folder_models_path):
        mkdir(folder_models_path)

    with open(models_file) as f:
        model_name = None
        model_lines = []
        for line in f:
            model_lines.append(line)
            if line == "//\n":
                with open(f"data/models_hmm/{model_name}.hmm", "w") as f_model:
                    f_model.writelines(model_lines)
                    model_lines = []
                    models.append(model_name)
                f_model.close()
            if line.startswith("NAME"):
                model_name = re.findall(REGEX_NAME, line)[0]
                conn = psycopg2.connect("dbname=%s user=%s  port=%s host=%s password=%s" % (db_name,user, db_port,db_host,password))
                cur = conn.cursor()
                cur.execute("INSERT INTO MODEL (code, path) VALUES (%s,%s)", (model_name,f"data/models_hmm/{model_name}.hmm"))
                conn.commit()
                cur.close()
                conn.close()
    f.close()
    return models


def get_proteins(model: str) -> List[str]:
    """Compute hmmsearch and returns the list of matching proteins."""
    output_file= f"data/models_txt/{model}.txt"
    command_line = 'hmmsearch --pfamtblout ' + output_file + f' data/models_hmm/{model}.hmm ' +  UNIPROT_DATABASE
    args = shlex.split(command_line)
    subprocess.call(args)
    proteins = get_proteins_from_hmmsearch_file(output_file)
    os.remove(output_file)
    return proteins


def get_proteins_from_hmmsearch_file(output_file: str) -> List[str]:
    with open(output_file) as file:
        proteins = []
        for line in file:
            if line.startswith("sp|"):
                protein = re.findall(REGEX_PROTEIN, line)[0]
                if protein not in proteins:
                    proteins.append(protein)
    file.close()
    return proteins
