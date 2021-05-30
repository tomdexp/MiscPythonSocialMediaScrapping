import sqlite3
import pandas as pd
import sys

profile_structure = "profile_ID,profileUrl,subCount,userName,profileDesc"
post_structure = "post_ID,postUrl,postText,pubDate,commentCount,likeCount,profileUrl"
relation_structure = "relation_ID, username_following,username_followed"

# Take a sqlite database file name path as an argument, return the connection object to the sqlite database
# example : create_connection("twitter_database")
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# Take a csv file name path as an argument, return a list containing the rows of the csv
# example : createRowListFromCsv("twitter_profile")
def createRowListFromCsv(csvFileName):
    df = pd.read_csv(csvFileName + ".csv", encoding="UTF-8", header=None)
    rowList = df.values.tolist()
    for row in rowList:
        row.insert(0, None)
    return rowList

# Take a connection object, a list, a sqlite request and a name of a sqlite table as arguments,
# is used to insert each element from the list in the sqlite table
def insertRowOneByOne(conn, rowList, sql, tableName):
    cur = conn.cursor()
    rowCountUnique = 0
    rowCountDupe = 0
    for row in rowList:
        try:
            cur.execute(sql, row)
            rowCountUnique += 1
        except sqlite3.IntegrityError:
            rowCountDupe += 1
    print(tableName, ': We have inserted', rowCountUnique, 'records to the table')
    print(tableName, ': There were', rowCountDupe, 'records that were already there in the table')
    return cur.lastrowid

# Take a connection object, a list and a sqlite request as arguments,
# is used to insert a entire list in a sqlite database
def insertRow(conn, rowList, sql):
    cur = conn.cursor()
    cur.executemany(sql, rowList)
    print('We have inserted', cur.rowcount, 'records to the table.')
    return cur.lastrowid

# Take a sqlite table name and a table structure string as arguments,
# return the sqlite request depending on the table structure string argument
def createSqlInsert(tableName,tableStructure):
    i = len(tableStructure.split(","))
    columncount = "".join("?," for _ in range(i))
    columncount = columncount[:-1]
    return ''' INSERT INTO {tablename}({columnsnames})
               VALUES({columncount}) '''.format(
        tablename=tableName,
        columnsnames=tableStructure,
        columncount=columncount,
    )

# Take a csv file name path, a sqlite database file name path, a sqlite table name and a table structure string
# as arguments, is used to convert a csv file into a sqlite database
# example : csvToSqlite("table_profile","twitter_db_v1", "table_profile", profile_structure)
def csvToSqlite(csvFileName, dbFileName, tableName, tableStructure):
    conn = create_connection(dbFileName + ".db")  # connect to sqlite database with system path
    rowList = createRowListFromCsv(csvFileName)
    sql = createSqlInsert(tableName, tableStructure)
    insertRowOneByOne(conn,rowList, sql, tableName)
    applyForeignKeyProfileToPost(conn)
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return

# Take a sqlite database file name path and a sqlite table name as arguments, is used to reset the table, index included
# ask for confirmation before deleting everything from the table
# example : resetTable("twitter_db_v1","table_profile")
def resetTable(dbFileName, tableName):
    conn = create_connection(dbFileName + ".db")  # connect to sqlite database with system path
    cur = conn.cursor()
    while True:
        answer = input("Are you sure you want to delete all row from {} ?\n yes/no : ".format(tableName))
        if answer == "yes":
            break
        elif answer =="no":
            sys.exit(1)
        else:
            print("invalid answer")
    cur.execute('DELETE FROM {};'.format(tableName), );
    print('We have deleted', cur.rowcount, 'records from {}.'.format(tableName))
    cur.close()
    cur = conn.cursor()
    cur.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{}";'.format(tableName), );
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return

# Take a connection object as an argument, is used to connect the two table via a Foreign Key and using profileUrl
def applyForeignKeyProfileToPost(conn):
    cur = conn.cursor()
    sql = '''
    UPDATE table_post
    SET profile_ID = (SELECT table_profile.profile_ID FROM table_profile WHERE table_profile.profileUrl = table_post.profileUrl);'''
    cur.execute(sql, )
    print("Successfully applied {} foreigns keys from profile to post".format(cur.rowcount))
    return

def getTwitterUserInfoForRelation():
    return

# EXAMPLE : resetTable("vaccin_db","table_profile")
# EXAMPLE: resetTable("vaccin_db","table_post")

# EXAMPLE : csvToSqlite("vaccin_table_profile","vaccin_db", "table_profile", profile_structure)
# EXAMPLE : csvToSqlite("vaccin_table_post","vaccin_db", "table_post", post_structure)