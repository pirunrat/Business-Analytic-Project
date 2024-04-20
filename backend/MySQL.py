import pandas as pd
import mysql.connector

class MySQL:
    def __init__(self, db_name):
        # Initialize your database connection parameters
        try:
            self.db_host = 'localhost'
            self.db_user = 'root'
            self.db_password = 'Pirunrat37@'
            self.db_name = db_name
            
            
             # Connect to the MySQL database
            self.conn = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
        except KeyError as e:
            print(f'Error MySQL connection : {e}')

    def mysql_load(self, query):
        # Execute the SQL query and fetch the data into a DataFrame
        df = pd.read_sql_query(query, self.conn)
        return df



# query = 'SELECT * FROM loan WHERE UNIQUEID = 417430'
# db_name = 'data_warehouse'
# sql = MySQL(db_name)
# df = sql.mysql_load(query)
# print(df)