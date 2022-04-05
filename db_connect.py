import MySQLdb

def connectToDB():
    connection = MySQLdb.connect('localhost', 'root', '', 'db_automation_test')
    cursor = connection.cursor()
    return connection, cursor
