    """
from collections import defaultdict

    def copy_mapping_virus_from_csv_to_dictionary(mapping_virus_file: str) -> List[str]:

        with open(mapping_virus_file) as f:
            mapping_virus_dictionary = defaultdict(list) for row in f:
            mapping_virus_dictionary[row[0]].append(row[1])
        f.close()
        return mapping_virus_dictionary

    def copy_mapping_host_from_tsv_to_dictionary(mapping_host_file: str) -> List[str]:

        with open(mapping_host_file) as f:
            mapping_host_dictionary = defaultdict(list) for row in f:
            mapping_host_dictionary[row[0]].append(row[1])
        f.close()
        return mapping_host_dictionary

    def copy_interactions_from_csv_to_dictionary(interactions_file: str) -> List[str]:

        with open(interactions_file) as f:
            interactions_dictionary = defaultdict(list) for row in f:
            interactions_dictionary[row[0]].append(row[1])
        f.close()
        return interactions_dictionary



    def host_proteins(protein: str, interactions_dictionary: List[str]) -> List[str]:

        host_proteins=[]
        string_host_proteins =[]

        string_protein_virus = {row[1] for row in mapping_virus_dictionary if row[2] == 'UniprotKB-EI' and row[1] == protein}
        string_host_proteins = get_interactions(string_protein_virus, interactions_dictionary)

        for string_host_protein in string_host_proteins:
            host_protein = {row[1] for row in mapping_host_dictionary if row[2] == string_host_protein}

            host_proteins.append(re.findall(REGEX_HOST_PROTEIN, host_protein))
            return host_proteins

    def get_interactions(string_protein_virus: str, interactions_dictionary: List[str]) -> List[str]:
        string_host_proteins = []

        string_host_protein = {row[1] for row in interactions_dictionary if row[0] == string_protein_virus}
        string_host_proteins.appen(string_host_protein)

        return string_host_proteins


    def save_interactions(protein: str, host_proteins: List[str]):
        for host_protein in host_proteins:
            idProteinV = session.query(Protein.idProtein).filter(Protein.code == protein)
            idProteinH = session.query(Protein.idProtein).filter(Protein.code == host_protein)

            if session.query(session.query(Interaction).filter(and_(Interaction.c.idProteinV == idProteinV, Interaction.c.idProteinH == idProteinH)).exists()).scalar() is None:
                interaction = Interaction.insert().values(idProteinV = idProteinV, idProteinH = idProteinH)
                session.execute(interaction)

    """
