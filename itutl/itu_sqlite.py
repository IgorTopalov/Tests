"""
  Custom ad hoc utilities to deal with the SQL Lite Db
     cur.execute('CREATE TABLE IF NOT EXISTS comments (book TEXT, volume INTEGER,   \
                              page INTEGER, userID TEXT, email TEXT, website TEXT, \
                              date TEXT, time TEXT, msgID INTEGER, line INTEGER,   \
                                   text TEXT, text_type TEXT)')
     cur.execute("CREATE INDEX comments_user ON comments (userID,msgID)")
     cur.execute("CREATE INDEX comments_user_all ON comments (userID,book,volume,page,msgID)")
     cur.execute("CREATE TABLE IF NOT EXISTS actions_log (key TEXT, status INTEGER)")
"""
import logging
import sqlite3
import sys
from logging import Logger
from sqlite3.dbapi2 import Connection

log: Logger = logging.getLogger(__name__ + "db_util")


def tables2check(conn):
    """
      Checks out whether this Db has been already initialized or not
      I.e. whether sqlite_master contains any custom tables

    """
    log.debug("Validate content of sqlite_master table")

    tables = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM sqlite_master")
    tables_all = {tup[1]: tup[0] for tup in cur.fetchall()}
    # indices are represented as tables (have type 'index')
    # system tables' names start in 'sqlite'
    for table, data_type in tables_all.items():
        if table.startswith("sqlite", 0, 7) or data_type != "table":
            continue  # =>>
        tables.append(table)
    log.debug("Tables found %s ", str(tables))
    return tables  # ##


def tables2create(conn, sql2exec: list):
    """

    :param conn:
    :type sql2exec: list
    """
    # --- initialize Db Schema - with a number of tables
    cur = conn.cursor()
    if sql2exec is None:
        return 0

    for sql in sql2exec:
        cur.execute(sql)

    log.info('Db schema initialized')
    conn.commit()
    return 1  # ###


def db_init(db_filename, sql2exec: list):
    if db_filename is None:
        raise Exception("Empty Db file name passed")

    try:
        conn: Connection = sqlite3.connect(db_filename)
    except:
        raise Exception(f"Invalid Db file reference {db_filename}. {sys.exc_info()[0]} ")

    tables = tables2check(conn)

    if len(tables) > 0:
        log.debug("Database already has been initialized!")
    else:
        log.debug("Initializing database!")
        tables2create(conn, sql2exec)
        tables = tables2check(conn)

    conn.close()

    return tables  # ##
