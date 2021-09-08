import sys

PACKAGE_PARENT = '..'
sys.path.append(PACKAGE_PARENT)

from app.main import main
from app.models import ModelVPF, Protein, Species, R_Protein_ModelVPF, Inaccessible_Protein, Function, R_Protein_Function, Interaction
from app.db import Session

model_expected = ['2029527005@ACOFG987_contig00088@ACOFGT_654600', '7000000001@SRS022530_LANL_scaffold_51249@SRS022530_LANL_scaffold_51249_gene_135542',
'2013843002@DCKB1_C2382@DCKB1_81390', '2029527005@ACOFG987_contig00088@ACOFGT_654830', '2029527005@ACOFG987_contig49236@ACOFGT_1385880']

inaccessible_protein_expected = ['A0A1D5NW84', 'E1C7K0', 'F1NUP4', 'F1NLJ3', 'A0A1D5NUL7']

protein_virus_expected = ['P25884', 'Q914J7', 'P04506', 'Q9QR71', 'Q4Z971', 'Q91G56', 'Q91FM3', 'Q91FM3', 'Q5UQL9', 'Q5UR22', 'Q5UQJ3', 'Q77MS1']

protein_model_expected = {"2029527005@ACOFG987_contig00088@ACOFGT_654600": ["P25884", "Q914J7", "P04506"],
"2029527005@ACOFG987_contig00088@ACOFGT_654830": ["Q5UQJ3"],
"2029527005@ACOFG987_contig49236@ACOFGT_1385880": ["Q77MS1"],
"2029527005@ACOFG987_contig00088@ACOFGT_654600": [""],
"7000000001@SRS022530_LANL_scaffold_51249@SRS022530_LANL_scaffold_51249_gene_1355142": ["Q9QR71", "Q4Z971", "Q91G56", "Q91FM3", "Q91FM3", "Q5UR22", "Q914J7",]}


protein_function = {"Q9QR71": ["GO:0042025", "GO:0003677", "GO:0039644"]}


protein_interaction_expected = {"Q77MS1": ["P18652", "P42683", "P09540", "E1C2C8", "A0A1D5NZV7", "Q7ZT63"]}

session = Session()


def test_main():
    #Code doesn't have errors
    TEST_MODEL_FILE = 'final_list_test.hmms'
    main(TEST_MODEL_FILE)


def test_model():
    #test models expected
    for model in model_expected:
        assert model == session.query(ModelVPF.code).filter(ModelVPF.code == model).scalar()

def test_protein_model():
    #test proteins expected
    for protein in protein_virus_expected:
        assert protein == session.query(Protein.codeUniprot).join(Species).filter(Protein.codeUniprot==protein).first()


    for model in protein_model_expected:
        set_protein = protein_model_expected[model]
        for p in set_protein:
            assert p == session.query(Protein.codeUniprot).join(R_Protein_ModelVPF.idProtein, R_Protein_ModelVPF.idProtein == Protein.idProtein).join(ModelVPF.idModel, ModelVPF.idModel == R_Protein_ModelVPF.idModel).filter(ModelVPF.code == model).scalar()

def inaccessible_protein():
    #test inaccessible protein expected
    for protein_inaccessible in inaccessible_protein_expected:
        assert protein_inaccessible == session.query(Protein.codeUniprot).filter(Protein.codeUniprot==protein_inaccessible).scalar()

def function():
    #test functions expected
    for protein in protein_function:
        set_function = protein_function[protein]
        for f in set_function:
            assert f == session.query(Function.codeGO).join(R_Protein_Function.c.idFunction, R_Protein_Function.c.idFunction == Function.idFunction).join(Protein.idProtein, Protein.idProtein == R_Protein_Function.c.idProtein).filter(Protein.codeUniProt == protein).scalar()


def interaction():
    #test interactions expected
    for proteinV in protein_interaction_expected:
        proteinsH = protein_interaction_expected[proteinV]
        for ph in proteinsH:
            assert ph == session.query(Interaction.c.idProteinH).join(Interaction.c.idProteinH, Interaction.c.idProteinH == Interaction.c.idProteinV).join(Protein.idProtein, Protein.idProtein == Interaction.c.idProteinV).filter(Protein.codeUniProt == proteinV).scalar()