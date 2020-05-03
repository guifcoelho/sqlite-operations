import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

def init():
    db_name = os.getenv('DB_NAME')
    conn = sqlite3.connect(f'{db_name}.db')
    return conn.cursor(), conn