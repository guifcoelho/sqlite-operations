import db.connection as connection

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    cursor, conn = connection.init()
    for command in sqlCommands:
        cursor.execute(command)

    conn.close()