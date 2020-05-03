from db.export.ExporterClass import Exporter

def run():
    tables_to_export = [
        {'name': 'table-name', 'file_to_export': 'path/to/file'}
    ]
    chunk_size = 500000
    for table in tables_to_export:
        Exporter(table['name'], table['file_to_export']).run(chunk_size)