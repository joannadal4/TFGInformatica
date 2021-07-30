import csv
from collections import defaultdict
from typing import List
from db import Session
from models import Protein, Interaction
from sqlalchemy.sql import exists, and_


def get_interactions(interactions_file: str) -> List[str]:
    interactions = defaultdict(list)
    with open(interactions_file) as f:
        rows = csv.reader(f, delimiter=" ")
        for row in rows:
            interactions[row[1]].append(row[0])

    return interactions




def save_interactions(protein: str, host_protein: str):

    session= Session()

    idProteinV = session.query(Protein.idProtein).filter(Protein.codeUniprot == protein)
    idProteinH = session.query(Protein.idProtein).filter(Protein.codeUniprot == host_protein)

    if session.query(exists().where(and_(Interaction.c.idProteinV == idProteinV, Interaction.c.idProteinH == idProteinH))).scalar() == False:

        interaction = Interaction.insert().values(idProteinV = idProteinV, idProteinH = idProteinH)
        session.execute(interaction)

    session.commit()
