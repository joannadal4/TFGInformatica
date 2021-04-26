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




def main() -> None:
    createUser()
    createDatabase()

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


if __name__ == "__main__":
    main()
