from psycopg2 import connect, errors


class PostgresID:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.table_name = "key_table"
        print("host = {}, port = {}".format(self.host, self.port))
        self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        self.conn = connect(
            dbname = self.dbname,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )

    def _rollback(self):
        cursor = self.conn.cursor()
        cursor.execute("ROLLBACK")
        cursor.close()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("CREATE TABLE {} (user_id varchar, pub_key varchar, aes_key varchar);".format(self.table_name))
            self.conn.commit()
            cursor.close()
            print("create table with name {}".format(self.table_name))

        except errors.DuplicateTable as e:
            print("Table {} already exists".format(self.table_name))
            self._rollback()

    def insert_user(self, user_id, pub_key, aes_key):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO {} VALUES ('{}', '{}', '{}')".format(self.table_name, user_id, pub_key, aes_key))
        self.conn.commit()
        cursor.close()

    def get_user_data(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE user_id = '{}'".format(self.table_name, user_id))
        fetch = cursor.fetchone()
        print(fetch)
        _, pub_key, aes_key = fetch
        self.conn.commit()
        cursor.close()
        return pub_key, aes_key
    
    def check_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE user_id = '{}'".format(self.table_name, user_id))
        fetch = cursor.fetchone()
        return fetch is not None
