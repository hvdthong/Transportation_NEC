__author__ = 'vdthoang'
import MySQLdb
def merge_database(list_source, target):

    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="facebook_bus") # name of the data base
    cur = db.cursor()
    list_table_target = []
    for schema in list_source:
        query_tables = "select table_name from information_schema.tables where table_schema='" + schema + "'"
        print query_tables
        cur.execute(query_tables)

        list_table = []

        for row in cur.fetchall():
            table = row[0]
            list_table.append(table)

        for table in list_table:
            if (table not in list_table_target):
                query_insert = "create table " + target + "." + table + " select * from " + schema + "." + table
                print query_insert
                cur.execute(query_insert)
                list_table_target.append(table)

    db.close()

        ## get all the tables for each schema

        ## for each table, add it to target schema

        ## if table appear in the target, don't add it


if __name__ == '__main__':

    list_source = ['facebook_bus', 'sgforums_singaporebuses', 'twitter_bus']
    target = '2015_allschemas'

    merge_database(list_source, target)