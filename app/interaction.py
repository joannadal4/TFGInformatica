import csv
from collections import defaultdict
from typing import List

from sqlalchemy.sql import exists, and_

from app.db import Session
from app.models import Protein, Interaction


def get_interactions(interactions_file: str) -> List[str]:
    """Create a list of interactions from a file text"""
    interactions = defaultdict(list)
    with open(interactions_file) as f:
        rows = csv.reader(f, delimiter=" ")
        for row in rows:
            interactions[row[1]].append(row[0])

    return interactions




def save_interaction(protein: str, host_protein: str):
    """Save the interaction to the database"""

    session= Session()
    idProteinV = session.query(Protein.idProtein).filter(Protein.codeUniprot == protein).scalar()
    idProteinH = session.query(Protein.idProtein).filter(Protein.codeUniprot == host_protein).scalar()

    if idProteinV is not None and idProteinH is not None:
        if session.query(exists().where(and_(Interaction.c.idProteinV == idProteinV, Interaction.c.idProteinH == idProteinH))).scalar() == False:
            interaction = Interaction.insert().values(idProteinV = idProteinV, idProteinH = idProteinH)
            session.execute(interaction)
            session.commit()

    session.close()
