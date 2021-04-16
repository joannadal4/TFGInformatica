-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2021-04-14 21:23:55.597

-- tables
-- Table: FUNCTION
CREATE TABLE FUNCTION (
    idFunction serial  NOT NULL,
    codeGO varchar(15)  NOT NULL,
    description varchar(200)  NOT NULL,
    aspect varchar(30)  NOT NULL,
    CONSTRAINT FUNCTION_pk PRIMARY KEY (idFunction)
);

-- Table: PROTEIN
CREATE TABLE PROTEIN (
    idProtein serial  NOT NULL,
    code varchar(15)  NOT NULL,
    name varchar(50)  NOT NULL,
    gene varchar(15)  NOT NULL,
    location varchar(100)  NOT NULL,
    idSpecie serial  NOT NULL,
    CONSTRAINT PROTEIN_pk PRIMARY KEY (idProtein)
);

-- Table: R_PROTEIN_FUNCTION
CREATE TABLE R_PROTEIN_FUNCTION (
    idProtein integer  NOT NULL,
    idFunction integer  NOT NULL,
    CONSTRAINT R_PROTEIN_FUNCTION_pk PRIMARY KEY (idFunction,idProtein)
);

-- Table: R_PROTEIN_MODELVPF
CREATE TABLE R_PROTEIN_MODELVPF (
    idProtein serial  NOT NULL,
    idModel serial  NOT NULL,
    score integer  NOT NULL,
    CONSTRAINT R_PROTEIN_MODELVPF_pk PRIMARY KEY (idProtein,idModel)
);

-- Table: R_PROTEIN_PROTEIN
CREATE TABLE R_PROTEIN_PROTEIN (
    idProteinV serial  NOT NULL,
    idProteinH serial  NOT NULL,
    CONSTRAINT R_PROTEIN_PROTEIN_pk PRIMARY KEY (idProteinH,idProteinV)
);

-- Table: SPECIE
CREATE TABLE SPECIE (
    idSpecie serial  NOT NULL,
    name varchar(50)  NOT NULL,
    taxonomy varchar(20)  NOT NULL,
    isVirus varchar(3)  NOT NULL,
    CONSTRAINT CHECK_0 CHECK (( ( isVirus in ( 'Yes' , 'No' ) ) )) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT SPECIE_pk PRIMARY KEY (idSpecie)
);

-- Table: VPFMODEL
CREATE TABLE VPFMODEL (
    idModel serial  NOT NULL,
    codeModel varchar(100)  NOT NULL,
    CONSTRAINT VPFMODEL_pk PRIMARY KEY (idModel)
);

-- foreign keys
-- Reference: FK_PROTEIN_SPECIE (table: PROTEIN)
ALTER TABLE PROTEIN ADD CONSTRAINT FK_PROTEIN_SPECIE
    FOREIGN KEY (idSpecie)
    REFERENCES SPECIE (idSpecie)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FK_R_PROTEIN_FUNCTION_FUNCTION (table: R_PROTEIN_FUNCTION)
ALTER TABLE R_PROTEIN_FUNCTION ADD CONSTRAINT FK_R_PROTEIN_FUNCTION_FUNCTION
    FOREIGN KEY (idFunction)
    REFERENCES FUNCTION (idFunction)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FK_R_PROTEIN_FUNCTION_PROTEIN (table: R_PROTEIN_FUNCTION)
ALTER TABLE R_PROTEIN_FUNCTION ADD CONSTRAINT FK_R_PROTEIN_FUNCTION_PROTEIN
    FOREIGN KEY (idProtein)
    REFERENCES PROTEIN (idProtein)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FK_R_PROTEIN_MODELVPF_PROTEIN (table: R_PROTEIN_MODELVPF)
ALTER TABLE R_PROTEIN_MODELVPF ADD CONSTRAINT FK_R_PROTEIN_MODELVPF_PROTEIN
    FOREIGN KEY (idProtein)
    REFERENCES PROTEIN (idProtein)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FK_R_PROTEIN_PROTEIN_PROTEINH (table: R_PROTEIN_PROTEIN)
ALTER TABLE R_PROTEIN_PROTEIN ADD CONSTRAINT FK_R_PROTEIN_PROTEIN_PROTEINH
    FOREIGN KEY (idProteinH)
    REFERENCES PROTEIN (idProtein)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FK_R_PROTEIN_PROTEIN_PROTEINV (table: R_PROTEIN_PROTEIN)
ALTER TABLE R_PROTEIN_PROTEIN ADD CONSTRAINT FK_R_PROTEIN_PROTEIN_PROTEINV
    FOREIGN KEY (idProteinV)
    REFERENCES PROTEIN (idProtein)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: R_PROTEIN_MODELVPF_VPFMODEL (table: R_PROTEIN_MODELVPF)
ALTER TABLE R_PROTEIN_MODELVPF ADD CONSTRAINT R_PROTEIN_MODELVPF_VPFMODEL
    FOREIGN KEY (idModel)
    REFERENCES VPFMODEL (idModel)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

