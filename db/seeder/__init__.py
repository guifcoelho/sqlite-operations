from db.seeder.SeederClass import Seeder
from db.seeder import stage_data_seeder

def run():
    seeders = [
        { 'table': 'name', 'path_to_data': 'path/to/data', 'fields': ['column1', 'column2', 'column3'] },
    ]
    
    for seeder in seeders:
        seeder = Seeder(seeder['table'],seeder['fields'],seeder['path_to_data'])
        if seeder.data_has_changed:
            seeder.run()

    stage_data_seeder.run()