from db.sql_scripts import executeScriptsFromFile

def run():
        sql_files = [
                'path/to/file'
        ]
        for sql_file in sql_files:
                executeScriptsFromFile(sql_file)
                print(f"Script SQL '{sql_file}' executado com sucesso")