import pyodbc
import config
import debug_logging_top_level


# SQL Commit
def call_sql_commit_dp_Contacts(client, serialnum, requestor):

    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    # Beginning in v. 18 it also will not connect without the TrustServerCertificate=yes par.
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + config.SERVER_NAME + ';DATABASE=' + config.DATABASE + ';ENCRYPT=yes;TrustServerCertificate=yes;UID=' + config.USER_NAME + ';PWD=' + config.PASSWORD)
    cursor = cnxn.cursor()
    cursor.execute("""INSERT INTO dbo.dp_Contacts (host_name, host_serialNum, cntct_requester) VALUES (?, ?, ?)""", client, serialnum, requestor)
    cursor.commit()
    debug_logging_top_level.send_log("Data Committed to SQL Table.")
    return


# db checks
def checkTableExists(tablename):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + config.SERVER_NAME + ';DATABASE=' + config.DATABASE + ';ENCRYPT=yes;TrustServerCertificate=yes;UID=' + config.USER_NAME + ';PWD=' + config.PASSWORD)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM sys.tables
        WHERE name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False


def checkIfEmpty (tableName):
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + config.SERVER_NAME + ';DATABASE=' + config.DATABASE + ';ENCRYPT=yes;TrustServerCertificate=yes;UID=' + config.USER_NAME + ';PWD=' + config.PASSWORD)
    qStr = 'SELECT * FROM [' + tableName + ']'
    debug_logging_top_level.send_log(qStr)
    cursor.execute(qStr)
    asd=cursor.fetchone()
    if asd==None:
        return True
    else:
        return False
