import psycopg2


def postgres_connection(dbname, user):
    """
    Returns connector to postgres
    :param dbname: name of database
    :param user: name of user
    :return: connector
    """
    conn = psycopg2.connect("host=localhost dbname={} user={}".format(dbname, user))
    return conn


def create_table(cur, conn, sql):
    """
    Function simply creates a table in the database
    :param cur: cursor to read/write to postgres
    :param conn: connector to
    :param sql: sql statement to be executed
    :return:
    """
    try:
        cur.execute(sql)
        conn.commit()
    except:
        print('something is wrong with the sql statement')
    print('table created')


def dump_to_db(cur, conn, full_path_to_data, delimiter, table_name):
    """
    Loads data into postgres the location and delimiter of the file
    :param cur: cursor to read/write to postgres
    :param conn: connector
    :param full_path_to_data: full path to data (including file)
    :param delimiter: delimiter of the file
    :param table_name: name of table to be written to
    :return: None
    """

    with open(full_path_to_data, 'r', encoding='utf-8') as f:
        next(f)
        cur.copy_from(f, table_name, sep=delimiter)
    conn.commit()
