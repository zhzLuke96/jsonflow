from src.parser import flow_parse,json_parse
from src.sql_factory import merge_sql

test1 = """{
    "{article}":{
        "!id":"=2",
        "...":"article"
    }
}"""

test2 = """{
"[user_arr]":{
    "name":"user.nick_name",
    "id":"user.c_ID",
    "amount":"user.u_amount",
    "{other}":"user...",
    "{record}":{
        "{last}":"top(record)",
        "[other]":"record..."
    }
}}"""

if __name__ == '__main__':
    from pprint import pprint
    j1 = json_parse(test1)
    j2 = json_parse(test2)
    pprint(j1.body[0][1]._dbs)
    print("sql:",merge_sql(j1.body[0][1]))
    pprint(j1.body[0][1].table)
    pprint(j2.body[0][1]._dbs)
    print("sql:",merge_sql(j2.body[0][1]))
    pprint(j2.body[0][1]._renames)
    pprint(j2.body[0][1].body)
    pprint(j2.body[0][1].table)
    # flow_parse(json_parse(test1))
    # flow_parse(json_parse(test2))
