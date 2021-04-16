import db
from tables import ModelVPF, Specie, Protein, Function, R_Protein_Function, R_Protein_Protein, R_Protein_ModelVPF


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
