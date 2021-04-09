import psycopg2
from psycopg2 import Error
from psycopg2 import sql

# postgres admin creds
admin_db_name = "testdb"
admin_db_user = "postgres"
admin_db_pass = "postgres"
db_host = "127.0.0.1"
db_port = "5432"

db_name = "virushost"
user = "joannadal"
password = "tfgInformatica_2021"


class DatabaseAdmin():
    def __init__(self):
        self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (admin_db_name,admin_db_user,db_host,admin_db_pass))
        self.conn.set_isolation_level(0)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        return self.cur.rowcount > 0

    def close(self):
        self.cur.close()
        self.conn.close()


class DatabaseTFG():
    def __init__(self):
        self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (db_name,user,db_host,password))
        self.conn.set_isolation_level(0)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        return self.cur.rowcount > 0

    def close(self):
        self.cur.close()
        self.conn.close()



def main() -> None:
    createUser()
    createDatabase()
    createTable()
    createIndex()


def createUser() -> None:

    check_user = ("SELECT 1 FROM pg_roles WHERE rolname='%s'" % (user))
    create_user = ("CREATE ROLE %s WITH LOGIN CREATEDB PASSWORD '%s'" % (user, password))

    db = DatabaseAdmin()
    user_exists = db.query(check_user)

    # PostgreSQL currently has no 'create role if not exists'
    # So, we only want to create the role/user if not exists else psycopg2
    if (user_exists) is True:
        print("%s user_exists: %s" % (user, user_exists))

    else:
        print("%s user_exists: %s" % (user, user_exists))
        print("Creating %s user now" % (user))
        db.query(create_user)
        user_exists = db.query(check_user)

    db.close()



def createDatabase() -> None:

    check_database = ("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '%s'" % (db_name))
    create_database  = ("CREATE DATABASE %s" % (db_name))

    db = DatabaseAdmin()
    database_exists = db.query(check_database)

    if (database_exists) is True:
        print("%s database_exists: %s" % (db_name, database_exists))

    else:
        print("%s database_exists: %s" % (db_name, database_exists))
        print("Creating %s database now" % (db_name))
        db.query(create_database)

    db.close()


def createTable() -> None:

    vpfmodel="vpfmodel"
    specie="specie"
    protein="protein"
    function="function"
    r_protein_function="r_protein_function"
    r_protein_modelvpf="r_protein_modelvpf"
    r_protein_protein="r_protein_protein"

    check_table_vpfmodel = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (vpfmodel))
    create_table_vpfmodel  = ("CREATE TABLE %s  (idModel   	SERIAL	 	PRIMARY KEY, codeModel	VARCHAR(100)	NOT NULL)" % (vpfmodel))

    check_table_specie = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (specie))
    create_table_specie  = ("CREATE TABLE %s  (idSpecie		SERIAL		PRIMARY KEY, name		VARCHAR(50)	NOT NULL, taxonomy	VARCHAR(20)	NOT NULL, isVirus    VARCHAR(3), CHECK (isVirus in ('Yes', 'No')))" % (specie))

    check_table_protein = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (protein))
    create_table_protein  = ("CREATE TABLE %s  (idProtein		SERIAL		PRIMARY KEY, code		VARCHAR(15)	NOT NULL, name		VARCHAR(50)	NOT NULL, gene		VARCHAR(15)	NOT NULL, location		VARCHAR(100)	NOT NULL, idSpecie		INTEGER	NOT NULL)" % (protein))
    create_fk_protein  = ("ALTER TABLE %s  ADD (CONSTRAINT       FK_PROTEIN_SPECIE FOREIGN KEY (idSpecie) REFERENCES SPECIE (idSpecie))" % (protein))

    check_table_function = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (function))
    create_table_function  = ("CREATE TABLE %s  (idFunction	SERIAL		PRIMARY KEY, codeGO		VARCHAR(15)	NOT NULL, description	VARCHAR(200)	NOT NULL, aspect		VARCHAR(30)	NOT NULL)" % (function))

    check_table_r_protein_function = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (r_protein_function))
    create_table_r_protein_function  = ("CREATE TABLE %s  (idProtein		SERIAL, idFunction	SERIAL, PRIMARY KEY (idProtein, idFunction))" % (r_protein_function))
    create_fk_r_protein_function  = ("ALTER TABLE %s  ADD (CONSTRAINT FK_R_PROTEIN_FUNCTION_PROTEIN FOREIGN KEY (idProtein) REFERENCES PROTEIN (idProtein), CONSTRAINT       FK_R_PROTEIN_FUNCTION_FUNCTION FOREIGN KEY (idFunction) REFERENCES FUNCTION (idFunction))" % (r_protein_function))

    check_table_r_protein_modelvpf = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (r_protein_modelvpf))
    create_table_r_protein_modelvpf  = ("CREATE TABLE %s  (idProtein		SERIAL, idModel		SERIAL, PRIMARY KEY (idProtein, idModel))" % (r_protein_modelvpf))
    create_fk_r_protein_modelvpf  = ("ALTER TABLE %s ADD (CONSTRAINT FK_R_PROTEIN_MODELVPF_PROTEIN FOREIGN KEY (idProtein) REFERENCES PROTEIN (idProtein), CONSTRAINT       FK_R_PROTEIN_MODELVPF_MODELVPF FOREIGN KEY (idModel)  REFERENCES MODELVPF (idModel))" % (r_protein_modelvpf))

    check_table_r_protein_protein = ("SELECT 1 FROM information_schema.tables WHERE table_name= '%s'" % (r_protein_protein))
    create_table_r_protein_protein = ("CREATE TABLE %s  (idProteinV	SERIAL, idProteinH	SERIAL, PRIMARY KEY (idProteinV, idProteinH))" % (r_protein_protein))
    create_fk_r_protein_protein  = ("ALTER TABLE %s ADD (CONSTRAINT FK_R_PROTEIN_PROTEIN_PROTEINV FOREIGN KEY (idProteinV) REFERENCES PROTEIN (idProtein), CONSTRAINT       FK_R_PROTEIN_PROTEIN_PROTEINH FOREIGN KEY (idProteinH)  REFERENCES PROTEIN (idProtein))" % (r_protein_protein))


    db = DatabaseTFG()

    table_vpfmodel_exists = db.query(check_table_vpfmodel)

    if (table_vpfmodel_exists) is True:
        print("%s table_vpfmodel_exists: %s" % (vpfmodel, table_vpfmodel_exists))

    else:
        print("%s table_vpfmodel_exists: %s" % (vpfmodel, table_vpfmodel_exists))
        print("Creating %s table now" % (vpfmodel))
        db.query(create_table_vpfmodel)


    table_specie_exists = db.query(check_table_specie)

    if (table_specie_exists) is True:
        print("%s table_specie_exists: %s" % (specie, table_specie_exists))

    else:
        print("%s table_specie_exists: %s" % (specie, table_specie_exists))
        print("Creating %s table now" % (specie))
        db.query(create_table_specie)


    table_protein_exists = db.query(check_table_protein)

    if (table_protein_exists) is True:
        print("%s table_protein_exists: %s" % (protein, table_protein_exists))

    else:
        print("%s table_protein_exists: %s" % (protein, table_protein_exists))
        print("Creating %s table now" % (protein))
        db.query(create_table_protein)
        db.query(create_fk_protein)


    table_function_exists = db.query(check_table_function)

    if (table_function_exists) is True:
        print("%s table_function_exists: %s" % (function, table_function_exists))

    else:
        print("%s table_function_exists: %s" % (function, table_function_exists))
        print("Creating %s table now" % (function))
        db.query(create_table_function)


    table_r_protein_function_exists = db.query(check_table_r_protein_function)

    if (table_r_protein_function_exists) is True:
        print("%s table_r_protein_function_exists: %s" % (r_protein_function, table_r_protein_function_exists))

    else:
        print("%s table_r_protein_function_exists: %s" % (r_protein_function, table_r_protein_function_exists))
        print("Creating %s table now" % (r_protein_function))
        db.query(create_table_r_protein_function)
        db.query(create_fk_r_protein_function)


    table_r_protein_modelvpf_exists = db.query(check_table_r_protein_modelvpf)

    if (table_r_protein_modelvpf_exists) is True:
        print("%s table_r_protein_modelvpf_exists: %s" % (r_protein_modelvpf, table_r_protein_modelvpf_exists))

    else:
        print("%s table_r_protein_modelvpf_exists: %s" % (r_protein_modelvpf, table_r_protein_modelvpf_exists))
        print("Creating %s table now" % (r_protein_modelvpf))
        db.query(create_table_r_protein_modelvpf)
        db.query(create_fk_r_protein_modelvpf)


    table_r_protein_protein_exists = db.query(check_table_r_protein_protein)

    if (table_r_protein_protein_exists) is True:
        print("%s table_r_protein_protein_exists: %s" % (r_protein_protein, table_r_protein_protein_exists))

    else:
        print("%s table_r_protein_protein_exists: %s" % (r_protein_protein, table_r_protein_protein_exists))
        print("Creating %s table now" % (r_protein_protein))
        db.query(create_table_r_protein_protein)
        db.query(create_fk_r_protein_protein)


    db.close()



def createIndex() -> None:

    index_fk_protein="index_fk_protein"
    index_fk_r_protein_function_protein="index_fk_r_protein_function_protein"
    index_fk_r_protein_function_function="index_fk_r_protein_function_function"
    index_fk_r_protein_modelvpf_protein="index_fk_r_protein_modelvpf_protein"
    index_fk_r_protein_modelvpf_modelvpf="index_fk_r_protein_modelvpf_modelvpf"
    index_fk_r_protein_protein_proteinv="index_fk_r_protein_protein_proteinv"
    index_fk_r_protein_protein_proteinh="index_fk_r_protein_protein_proteinh"


    check_index_fk_protein = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_protein))
    check_index_fk_r_protein_function_protein = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_r_protein_function_protein))
    check_index_fk_r_protein_function_function = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_r_protein_function_function))
    check_index_fk_r_protein_modelvpf_protein = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_r_protein_modelvpf_protein))
    check_index_fk_r_protein_modelvpf_modelvpf = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_r_protein_modelvpf_modelvpf))
    check_index_fk_r_protein_protein_proteinv = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_r_protein_protein_proteinv))
    check_index_fk_r_protein_protein_proteinh = ("SELECT 1 FROM pg_class c WHERE c.relname = '%s'" % (index_fk_r_protein_protein_proteinv))


    create_index_fk_protein  = "CREATE INDEX index_fk_protein ON protein (idSpecie)"
    create_index_fk_r_protein_function_protein  = "CREATE INDEX index_fk_r_protein_function_protein ON r_protein_function (idProtein)"
    create_index_fk_r_protein_function_function  = "CREATE INDEX index_fk_r_protein_function_function ON r_protein_function (idFunction)"
    create_index_fk_r_protein_modelvpf_protein  = "CREATE INDEX index_fk_r_protein_modelvpf_protein ON r_protein_modelvpf (idProtein)"
    create_index_fk_r_protein_modelvpf_modelvpf  = "CREATE INDEX index_fk_r_protein_modelvpf_modelvpf ON r_protein_modelvpf (idModel)"
    create_index_fk_r_protein_protein_proteinv  = "CREATE INDEX index_fk_r_protein_protein_proteinV ON r_protein_protein (idProteinv)"
    create_index_fk_r_protein_protein_proteinh  = "CREATE INDEX index_fk_r_protein_protein_proteinH ON r_protein_protein (idProteinh)"


    db = DatabaseTFG()

    index_fk_protein_exists = db.query(check_index_fk_protein)

    if (index_fk_protein_exists) is True:
        print("%s index_fk_protein_exists: %s" % (index_fk_protein, index_fk_protein_exists))

    else:
        print("%s index_fk_protein_exists: %s" % (index_fk_protein, index_fk_protein_exists))
        print("Creating %s index now" % (index_fk_protein))
        db.query(create_index_fk_protein)


    index_fk_r_protein_function_protein_exists = db.query(check_index_fk_r_protein_function_protein)

    if (index_fk_r_protein_function_protein_exists) is True:
        print("%s index_fk_r_protein_function_protein_exists: %s" % (index_fk_r_protein_function_protein, index_fk_r_protein_function_protein_exists))

    else:
        print("%s index_fk_r_protein_function_protein_exists: %s" % (index_fk_r_protein_function_protein, index_fk_r_protein_function_protein_exists))
        print("Creating %s index now" % (index_fk_r_protein_function_protein))
        db.query(create_index_fk_r_protein_function_protein)


    index_fk_r_protein_function_function_exists = db.query(check_index_fk_r_protein_function_function)

    if (index_fk_r_protein_function_function_exists) is True:
        print("%s index_fk_r_protein_function_function_exists: %s" % (index_fk_r_protein_function_function, index_fk_r_protein_function_function_exists))

    else:
        print("%s index_fk_r_protein_function_function_exists: %s" % (index_fk_r_protein_function_function, index_fk_r_protein_function_function_exists))
        print("Creating %s index now" % (index_fk_r_protein_function_function))
        db.query(create_index_fk_r_protein_function_function)


    index_fk_r_protein_modelvpf_protein_exists = db.query(check_index_fk_r_protein_modelvpf_protein)

    if (index_fk_r_protein_modelvpf_protein_exists) is True:
        print("%s index_fk_r_protein_modelvpf_protein_exists: %s" % (index_fk_r_protein_modelvpf_protein, index_fk_r_protein_modelvpf_protein_exists))

    else:
        print("%s index_fk_r_protein_modelvpf_protein_exists: %s" % (index_fk_r_protein_modelvpf_protein, index_fk_r_protein_modelvpf_protein_exists))
        print("Creating %s index now" % (index_fk_r_protein_modelvpf_protein))
        db.query(create_index_fk_r_protein_modelvpf_protein)


    index_fk_r_protein_modelvpf_modelvpf_exists = db.query(check_index_fk_r_protein_modelvpf_modelvpf)

    if (index_fk_r_protein_modelvpf_modelvpf_exists) is True:
        print("%s index_fk_r_protein_modelvpf_modelvpf_exists: %s" % (index_fk_r_protein_modelvpf_modelvpf, index_fk_r_protein_modelvpf_modelvpf_exists))

    else:
        print("%s index_fk_r_protein_modelvpf_modelvpf_exists: %s" % (index_fk_r_protein_modelvpf_modelvpf, index_fk_r_protein_modelvpf_modelvpf_exists))
        print("Creating %s index now" % (index_fk_r_protein_modelvpf_modelvpf))
        db.query(create_index_fk_r_protein_modelvpf_modelvpf)


    index_fk_r_protein_protein_proteinv_exists = db.query(check_index_fk_r_protein_protein_proteinv)

    if (index_fk_r_protein_protein_proteinv_exists) is True:
        print("%s index_fk_r_protein_protein_proteinv_exists: %s" % (index_fk_r_protein_protein_proteinv, index_fk_r_protein_protein_proteinv_exists))

    else:
        print("%s index_fk_r_protein_protein_proteinv_exists: %s" % (index_fk_r_protein_protein_proteinv, index_fk_r_protein_protein_proteinv_exists))
        print("Creating %s index now" % (index_fk_r_protein_protein_proteinv))
        db.query(create_index_fk_r_protein_protein_proteinv)


    index_fk_r_protein_protein_proteinh_exists = db.query(check_index_fk_r_protein_protein_proteinh)

    if (index_fk_r_protein_protein_proteinh_exists) is True:
        print("%s index_fk_r_protein_protein_proteinh_exists: %s" % (index_fk_r_protein_protein_proteinh, index_fk_r_protein_protein_proteinh_exists))

    else:
        print("%s index_fk_r_protein_protein_proteinh_exists: %s" % (index_fk_r_protein_protein_proteinh, index_fk_r_protein_protein_proteinh_exists))
        print("Creating %s index now" % (index_fk_r_protein_protein_proteinh))
        db.query(create_index_fk_r_protein_protein_proteinh)


    db.close()

def insert() -> None:

    insertExample = ("INSERT INTO a_table (c1, c2, c3) VALUES('%s', '%s', '%s')" % (v1, v2, v3))

    db = DatabaseTFG()
    db.query(insertExample)
    db.close()

if __name__ == "__main__":
    main()
