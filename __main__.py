import db.create_tables as create_tables
import db.seeder as seeder
import db.join_tables as join_tables
import db.export as export
import sys
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    if 'reset' in sys.argv:
        os.remove(f"{os.getenv('DB_NAME')}.db")
    create_tables.run()
    seeder.run()
    join_tables.run()
    export.run()

if __name__ == '__main__':
    main()