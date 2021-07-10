import pandas.io.sql as psql
import pyodbc


# to call a class's function within the same class, use self.function_name

class MsSqlClass:

    def __init__(self):
        ms_sql_server = ""
        user = ""
        password = ""
        connection_str = f"DSN={ms_sql_server};UID={user};PWD={password}"
        self.conn = pyodbc.connect(connection_str)
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def run_query(self):
        try:
            self.cur.execute("query")
            self.commit()

        except Exception as e:
            print(e)
            self.rollback()

    def get_data(self):
        data = psql.read_sql("query", self.conn)  # runs sql query and returns pandas df
