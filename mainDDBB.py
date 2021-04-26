import db
from models import ModelVPF, Species, Protein, Function, R_Protein_Function, Interaction, R_Protein_ModelVPF


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
