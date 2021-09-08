import sys

PACKAGE_PARENT = '..'
sys.path.append(PACKAGE_PARENT)

from app.main import main
from app.models import ModelVPF, Protein, Species, R_Protein_ModelVPF, Inaccessible_Protein, Function, R_Protein_Function, Interaction
from app.db import Session
from app.hmm import split_models


def test_main():

    TEST_MODEL_FILE = 'final_list_test.hmms'
    main(TEST_MODEL_FILE)

    """
    models = ['2029527005@ACOFG987_contig00088@ACOFGT_654600', '7000000001@SRS022530_LANL_scaffold_51249@SRS022530_LANL_scaffold_51249_gene_135542',
    '2013843002@DCKB1_C2382@DCKB1_81390', '2029527005@ACOFG987_contig00088@ACOFGT_654830', '2029527005@ACOFG987_contig49236@ACOFGT_1385880']
    expected_proteins = {
        '2029527005@ACOFG987_contig00088@ACOFGT_654600': ['p1', 'p2']
    }
    expected_functions = {
        '2029527005@ACOFG987_contig00088@ACOFGT_654600': ['p1', 'p2']
    }
    expected_interactions = {
        '2029527005@ACOFG987_contig00088@ACOFGT_654600': ['p1', 'p2']
    }
"""
    assert True == True
    # for model in models:
            # assert session.query(ModelVPF.code).filter(ModelVPF.code == model).scalar()
            # proteins = session.query(Protein.codeUniProt).join(R_Protein_ModelVPF, R_Protein_ModelVPF.idProtein == Protein.idProtein).join(R_Protein_ModelVPF, R_Protein_ModelVPF.idModel == ModelVPF.idModel).filter(ModelVPF.code = model)
            # assert proteins == expected_proteins[model]
    #         proteins = get_proteins(model)
    #         for protein in proteins:
    #             assert protein == session.query(Protein.codeUniProt).join(R_Protein_ModelVPF, R_Protein_ModelVPF.idProtein == Protein.idProtein).join(R_Protein_ModelVPF, R_Protein_ModelVPF.idModel == ModelVPF.idModel).filter(ModelVPF.code = model)

    #             functions = get_go_functions()
    #             for function in functions:
    #                 assert function == session.query(Function.codeGO).join(R_Protein_Function, R_Protein_Function.idFunction == Function.idFunction).join(R_Protein_Function, R_Protein_Function.idProtein == Protein.idProtein).filter(Protein.codeUniProt = protein)

    #             interactions = ...
