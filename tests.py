from src.parser import json_parse
from src.executor import executor
from src.sqlite_factory import simple as factory

test1 = """{
    "[admins]":{
        "!nick_name":"like 'admin_%'",
        "!sex":"= 'male'",
        "id":"user.u_id",
        "name":"user.nick_name",
        "...":"user"
    }
}"""

test2 = """{
"[user_arr]":{
    "!nick_name":"like 'admin_%'",
    "!sex":"= 'male'",
    "name":"user.nick_name",
    "id":"user.u_id",
    "amount":"user.u_amount",
    "?rich":"amount > 100",
    "...":"user",
    "{orders}":{
        "...":"orders"
    }
}}"""

test3 = """{
    "{sys_status}":{
        "cpu":"%cpu_status",
        "memory_free":"%memory_status"
    }
}"""


def get_cpu_status():
    import psutil
    return psutil.cpu_percent(interval=1)


def get_mem_status():
    import psutil
    return psutil.virtual_memory().percent


if __name__ == '__main__':
    # print(sql_show("t.db"))
    # print(sql_field_name("t.db"))

    from pprint import pprint
    # j1 = json_parse(test1)
    f1 = factory("./tests/t.db")
    f1.variable["cpu_status"] = get_cpu_status
    f1.variable["memory_status"] = get_mem_status
    # e1 = executor(test1, f1)
    # pprint(e1.dump())
    e2 = executor(test2, f1)
    print(e2.flow.body[0][1].body)
    pprint(e2.dump())
    # print(e2.flow.body[0][1].body[1][1].query)
    # print(j1.body[0][1].query["item"])
    # print(j1.body[0][1]._renames)
    # print(dict(j1.body))
    # print(j1.body[0][1].body)
    # print(list(sqlite_do(j1.body[0][1].script, "t.db")))
    # pprint(j1.body[0][1]._dbs)
    # print("sql:",merge_sql(j1.body[0][1]))
    # pprint(j1.body[0][1].table)
    # j2 = json_parse(test2)
    # pprint(j2.body[0][1]._dbs)
    # print("sql:",merge_sql(j2.body[0][1]))
    # pprint(j2.body[0][1]._renames)
    # pprint(j2.body[0][1].body)
    # pprint(j2.body[0][1].table)
    # flow_parse(json_parse(test1))
    # flow_parse(json_parse(test2))
