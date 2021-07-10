import psycopg2

insert = "INSERT INTO {} (col1, col2) VALUES ({});".format
insert_return_id = "INSERT INTO {} (col1, col2) VALUES ({}) RETURNING id;".format

update = "UPDATE {} SET col_name={} WHERE col1=val1;".format

delete = "delete table_name WHERE col=val;"


class PgUtility:

    def __init__(self):
        pg_server = ""
        pg_db = ""
        user = ""
        pwd = ""
        conn_str = f"dbname={pg_db} user={user} host={pg_server} password={pwd}"
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

    def insert_return_id(self):
        insert_command = insert_return_id("table_name", ["val1", "val2"])
        self.cur.execute(insert_command)
        return_id = self.cur.fetchone()[0]
        self.conn.commit()
        return return_id
