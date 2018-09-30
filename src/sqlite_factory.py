
__all__ = ("simple",)


def sqlite_do(script, file_name):
    import sqlite3

    with sqlite3.connect(file_name) as conn:
        c = conn.cursor()
        return c.execute(script)


def sql_field_name(file_name, table_name):
    return [r[1] for r in list(sqlite_do(f"PRAGMA table_info([{table_name}])", file_name))]


def sql_foreign_key(file_name, table_name):
    return list(sqlite_do(f"PRAGMA foreign_key_list([{table_name}])", file_name))


def sql_table_name(file_name):
    return list(sqlite_do("select name from sqlite_master where type='table' order by name;", file_name))


class simple(object):
    def __init__(self, file_name):
        self.db_file = file_name

    def commit(self, s):
        return sqlite_do(s, self.db_file)

    def foreign_key(self, t1, t2):
        return [r[3:5] for r in sql_foreign_key(self.db_file, t1) if r[2] == t2]

    def get_keys(self, table):
        return sql_field_name(self.db_file, table)

    def table_is_save(self, table):
        return table in slef.tables()

    def tables(self):
        return sql_table_name(self.db_file)
