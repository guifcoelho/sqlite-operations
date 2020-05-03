from db.sql_scripts import executeScriptsFromFile

def run():

        executeScriptsFromFile('db/sql_scripts/create_metadata_tables_table.sql')

        tables_to_reset = [
                'path/to/script',
        ]

        for table in tables_to_reset:
                executeScriptsFromFile(table)

        print('Tabelas (re)criadas com sucesso.')