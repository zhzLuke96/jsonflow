

def merge_sql(flow):
    table_name, sql_arr = flow.table, flow._dbs
    wheres = [r[1] for r in sql_arr if "where" in r[0]]
    items = [r[1] for r in sql_arr if "item" in r[0]]
    item_sql = "*" if len(items) == 0 else ",".join(items)
    where_sql = "" if len(wheres) == 0 else ("WHRER " + " AND ".join(wheres))

    return f"SELECT {item_sql} FROM {table_name} {where_sql}"
