import MySQLdb

def connectToDB():
    connection = MySQLdb.connect('localhost', 'root', '', 'automation_test')
    cursor = connection.cursor()
    return connection, cursor
