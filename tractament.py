def mapping_host():
    with open("protein_aliases_host.tsv") as f:
        for line in f:
            args_line= line.split()
            with open("protein_host_mapping.txt", "a") as file:
                line_to_save = args_line[2] +  "\t" + args_line[1].split('|')[0] + "\n"
                file.write(line_to_save)
            file.close()
    f.close()



def mapping_virus():
    with open("protein_aliases_virus.txt") as f:
        for line in f:
            args_line= line.split()
            with open("protein_virus_mapping.txt", "a") as file:
                if args_line[2] == "UniProtKB-EI":
                    line_to_save = args_line[0] +  "\t" + args_line[1]
                    file.write(line_to_save)
            file.close()
    f.close()



if __name__ == "__main__":
    mapping_host()
    mapping_virus()
