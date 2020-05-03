import db.connection as connection
import math
import csv

class Exporter():
    def __init__(self, table: str, file_path_to_export:str):
        self.table = table
        self.file_path_to_export = file_path_to_export
        self.cursor, self.conn = connection.init()

    def __getTableColumnNames__(self)->list:
        self.cursor.execute(f"PRAGMA table_info({self.table})")
        result = self.cursor.fetchall()
        return [row[1] for row in result]

    def __initFileToExport__(self)->None:
        column_names = self.__getTableColumnNames__()
        with open(self.file_path_to_export, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
        f.close()

    def run(self, chunk_size:int = 1000000)->None:
        self.__initFileToExport__()
        self.cursor.execute(f"SELECT COUNT(0) FROM {self.table};")
        nrows = self.cursor.fetchone()[0]
        chunks_to_export = math.ceil(nrows/chunk_size)
        print(f"Exportando dados para '{self.file_path_to_export}' ({nrows} linhas)")
        for i in range(chunks_to_export):
            self.cursor.execute(f"SELECT * FROM {self.table} LIMIT {chunk_size} OFFSET {i * chunk_size};")
            result = self.cursor.fetchall()
            with open(self.file_path_to_export, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(result)
            f.close()
            print(f"Progresso: {100*round((i+1)/chunks_to_export,2)}%")

        self.conn.close()