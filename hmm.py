import re
import subprocess, shlex
import tempfile
import os
from os import mkdir
from typing import List
from time import sleep

from config import UNIPROT_DATABASE
from constant import REGEX_NAME, REGEX_PROTEIN, REGEX_SPECIE, E_VALUE_COLUMN, SCORE_COLUMN

from models import ModelVPF, Protein, Species, R_Protein_ModelVPF
from db import Session

import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree

from sqlalchemy.sql import exists

from mapping import PROTEIN_MAPPING_STRING

def split_models(models_file: str) -> List[str]:
    """Get one model files, split in one file per model and returns the model names."""
    models = []
    folder_models_path = "data/models_hmm"
    if not os.path.exists("data"):
        mkdir("data")
    if not os.path.exists(folder_models_path):
        mkdir(folder_models_path)

    session= Session()

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
            if line.startswith("NAME"):
                model_name = re.findall(REGEX_NAME, line)[0]
                if session.query(exists().where(ModelVPF.code == model_name)).scalar() == False:
                    modelvpf = ModelVPF(code=model_name, path=f"data/models_hmm/{model_name}.hmm")
                    session.add(modelvpf)
                    session.commit()
    session.close()

    return models


def get_proteins(model: str) -> List[str]:
    """Compute hmmsearch and returns the list of matching proteins."""

    session= Session()
    folder_models_txt = "data/models_txt"
    if not os.path.exists(folder_models_txt):
        mkdir(folder_models_txt)
    output_file= f"data/models_txt/{model}.txt"

    proteins = []
    idModel = session.query(ModelVPF.idModel).filter(ModelVPF.code == model)
    if session.query(exists().where(R_Protein_ModelVPF.idModel == idModel)).scalar() == False:

        cl_hmmpress = f"hmmpress data/models_hmm/{model}.hmm"
        args_hmmpress = shlex.split(cl_hmmpress)
        subprocess.call(args_hmmpress)

        cl_hmmscan = f"hmmscan --tblout {output_file} data/models_hmm/{model}.hmm {UNIPROT_DATABASE}"   #--incE {threshold} (e.value > 0.001)
        args_hmmscan = shlex.split(cl_hmmscan)
        subprocess.call(args_hmmscan)

        proteins = get_proteins_from_hmmscan_file(output_file, model)


        for protein in proteins:

            score_evalue = get_score_evalue_protein_model(output_file, protein, model)
            save_protein(protein, True, session=session)

            idProtein = session.query(Protein.idProtein).filter(Protein.codeUniprot == protein)
            if session.query(exists().where(R_Protein_ModelVPF.idProtein == idProtein and R_Protein_ModelVPF.idModel == idModel)).scalar() == False:
                if score_evalue is not None:
                    model_protein = R_Protein_ModelVPF(idProtein = idProtein, idModel = idModel, score = score_evalue[0], e_value = score_evalue[1])
                    session.add(model_protein)
                    session.commit()

                else:
                    model_protein = R_Protein_ModelVPF(idProtein = idProtein, idModel = idModel)
                    session.add(model_protein)
                    session.commit()

    session.close()
    return proteins


def save_protein(protein: str, isVirus=False, session=None):
    """Save a protein to the database"""

    new_session = session is None

    session = session or Session()
    code_string_protein = PROTEIN_MAPPING_STRING.get(protein)

    if session.query(exists().where(Protein.codeUniprot == protein)).scalar() == False:
        try:
            response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
        except:
            sleep(5)
            response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")

            # parse xml and return protein information
        try:
            root = ElementTree.fromstring(response.content)

            taxonomy = root.findall('.//{http://uniprot.org/uniprot}lineage')[0][-1].text

            gene = root.findall('.//{http://uniprot.org/uniprot}gene')
            if len(gene)>0:
                gene = root.findall('.//{http://uniprot.org/uniprot}gene')[0][0].text

            name_species = root.findall('.//{http://uniprot.org/uniprot}organism')[0][0].text
            if (name_species.find('(') > -1):
                name_species = re.findall(REGEX_SPECIE, name_species)[0]

            name_protein = root.findall('.//{http://uniprot.org/uniprot}fullName')[0].text

            subcellularLocation = []
            location = root.findall('.//{http://uniprot.org/uniprot}subcellularLocation')
            for child in location:
                if child[0].text not in subcellularLocation:
                    subcellularLocation.append(child[0].text)

            location = ""
            for child in subcellularLocation:
                location = child + ', ' + location

            if session.query(exists().where(Species.name == name_species)).scalar() == False:
                species = Species(name=name_species, taxonomy=taxonomy, isVirus = isVirus)
                session.add(species)
                session.commit()

            idSpecies = session.query(Species.idSpecies).filter(Species.name == name_species)
            object_protein = Protein(codeUniprot = protein, codeString = code_string_protein, name = name_protein, gene = gene, location = location, idSpecies = idSpecies)
            session.add(object_protein)
            session.commit()

        except:
            print(f"The protein {protein} doesn't exists")


    if new_session:
        session.close()

def get_score_evalue_protein_model(output_file: str, protein: str, model: str) -> str:
    """Get the parameters score and e-value from the resulting file after hmmscan"""
    with open(output_file) as file:
        score_evalue = []
        for line in file:
            if line.startswith(f"{model} -          sp|{protein}"):
                line_list = line.split()
                return line_list[E_VALUE_COLUMN], line_list[SCORE_COLUMN]


def get_proteins_from_hmmscan_file(output_file: str, model: str) -> List[str]:
    """Get the proteins which belong a model"""
    with open(output_file) as file:
        proteins = []
        for line in file:
            if line.startswith(model):
                protein = re.findall(REGEX_PROTEIN, line)[0]
                if protein not in proteins:
                    proteins.append(protein)
    return proteins
