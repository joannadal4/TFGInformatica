import re
import subprocess, shlex
import tempfile
import os
from os import mkdir
from typing import List
from time import sleep

from config import UNIPROT_DATABASE
from constant import REGEX_NAME, REGEX_PROTEIN, REGEX_SPECIE

from models import ModelVPF, Protein, Species, R_Protein_ModelVPF
from db import Session

import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree

from sqlalchemy.sql import exists



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
        session= Session()
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
                if session.query(exists().where(ModelVPF.code == model_name)).scalar() == False:
                    modelvpf = ModelVPF(code=model_name, path=f"data/models_hmm/{model_name}.hmm")
                    session.add(modelvpf)
        session.commit()
    f.close()
    return models


def get_proteins(model: str) -> List[str]:
    """Compute hmmsearch and returns the list of matching proteins."""
    folder_models_txt = "data/models_txt"
    if not os.path.exists(folder_models_txt):
        mkdir(folder_models_txt)
    output_file= f"data/models_txt/{model}.txt"
    command_line = 'hmmpress ' + f'data/models_hmm/{model}.hmm'
    args = shlex.split(command_line)
    subprocess.call(args)
    command_line = 'hmmscan --tblout ' + output_file + f' data/models_hmm/{model}.hmm ' +  UNIPROT_DATABASE   #--incE {threshold} (e.value > 0.001)
    args = shlex.split(command_line)
    subprocess.call(args)

    proteins = get_proteins_from_hmmscan_file(output_file, model)

    session= Session()

    for protein in proteins:
        score_evalue = get_score_evalue_protein_model(output_file, protein, model)

        try:
            response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
        except:
            sleep(5)
            response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
        # parse xml and return protein information
        root = ElementTree.fromstring(response.content)


        taxonomy = root.findall('.//{http://uniprot.org/uniprot}lineage')[0][-1].text

        gene = root.findall('.//{http://uniprot.org/uniprot}gene')
        if len(gene)>0:
            gene = root.findall('.//{http://uniprot.org/uniprot}gene')[0][0].text

        name_species = root.findall('.//{http://uniprot.org/uniprot}organism')[0][0].text
        if (name_species.find('(') > -1):
            name_species = re.findall(REGEX_SPECIE, name_species)[0]

        name_protein = root.findall('.//{http://uniprot.org/uniprot}recommendedName')[0][0].text

        subcellularLocation = []
        location = root.findall('.//{http://uniprot.org/uniprot}subcellularLocation')
        for child in location:
            if child[0].text not in subcellularLocation:
                subcellularLocation.append(child[0].text)

        location = ""
        for child in subcellularLocation:
            location = child + ', ' + location

        if session.query(exists().where(Species.name == name_species)).scalar() == False:
            species = Species(name=name_species, taxonomy=taxonomy, isVirus = True)
            session.add(species)

        if session.query(exists().where(Protein.code == protein)).scalar() == False:
            idSpecies = session.query(Species.idSpecies).filter(Species.name == name_species)
            prot = Protein(code = protein, name = name_protein, gene = gene, location = location, idSpecies = idSpecies)
            session.add(prot)


        idProtein = session.query(Protein.idProtein).filter(Protein.code == protein)
        idModel = session.query(ModelVPF.idModel).filter(ModelVPF.code == model)
        if session.query(exists().where(R_Protein_ModelVPF.idProtein == idProtein and R_Protein_ModelVPF.idModel == idModel)).scalar() == False:
            model_protein = R_Protein_ModelVPF(idProtein = idProtein, idModel = idModel, score = score_evalue[0], e_value = score_evalue[1])
            session.add(model_protein)

    session.commit()

    return proteins

def get_score_evalue_protein_model(output_file: str, protein: str, model: str) -> str:
    with open(output_file) as file:
        score_evalue = []
        for line in file:
            if line.startswith(f"{model} -          sp|{protein}"):
                score_evalue.append(line.split()[5])
                score_evalue.append(line.split()[4])
    file.close()
    return score_evalue


def get_proteins_from_hmmscan_file(output_file: str, model: str) -> List[str]:
    with open(output_file) as file:
        proteins = []
        for line in file:
            if line.startswith(model):
                protein = re.findall(REGEX_PROTEIN, line)[0]
                if protein not in proteins:
                    proteins.append(protein)
    file.close()
    return proteins
