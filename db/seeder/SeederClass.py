import pandas as pd
import db.connection as connection
import os

class Seeder():
   
    def __init__(self, table:str, fields:list, path_to_data:str = ""):
       self.table:str = table
       self.path_to_data:str = path_to_data
       self.fields:list = fields

    @property
    def has_data(self):
        cursor, conn = connection.init()
        cursor.execute(f"SELECT COUNT(0) FROM {self.table}")
        result = cursor.fetchone()[0] > 0
        conn.close()
        return result

    def get_file_modified_at_hash(self):
        return self.table+'-'+str(hash(os.path.getmtime(self.path_to_data)))

    def fetch_modified_at_hash(self):
        cursor, conn = connection.init()
        cursor.execute(f"SELECT load_hash FROM metadata_tables WHERE table_name='{self.table}'")       
        result = cursor.fetchone()
        if result is not None:
            result = result[0]
        conn.close()
        return result

    @property
    def data_has_changed(self):
        file_hash = self.get_file_modified_at_hash()
        table_hash = self.fetch_modified_at_hash()
        return file_hash != table_hash

    def run(self, data = None, chunk = 1):
        cursor, conn = connection.init()
        if data is None:
            data = pd.read_csv(self.path_to_data, sep=";", encoding="iso-8859-1").to_numpy()

        query_field = ",".join(self.fields)
        query_question_marks = ','.join(['?' for field in self.fields])
        cursor.executemany(f"INSERT INTO {self.table} ({query_field}) VALUES ({query_question_marks})", data)
        file_hash = self.update_hash(cursor, conn)
        conn.commit()
        print(f"Seeder '{self.table}' executado com sucesso (chunk {chunk}) - hash: {file_hash}")
        conn.close()

    def update_hash(self, cursor, conn, commit = False):        
        file_hash = self.get_file_modified_at_hash()
        cursor.execute(f"SELECT COUNT(0) FROM metadata_tables WHERE table_name='{self.table}'")
        
        if cursor.fetchone()[0] == 0:
            cursor.execute(f"INSERT INTO metadata_tables (table_name, load_hash) VALUES ('{self.table}', '{file_hash}')")
        else:
            cursor.execute(f"UPDATE metadata_tables SET load_hash='{file_hash}' WHERE table_name='{self.table}'")
        
        if commit:
            conn.commit()

        return file_hash
