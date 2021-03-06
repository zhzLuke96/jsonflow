import copy
from .parser import json_parse
from .flow import Json_flow
from .mod import call_watch, call_plugin

__all__ = ("executor",)


def get_new_keys(flow, fact):
    if flow.is_query_all_item:
        keys = fact.get_keys(flow.table)
    else:
        keys = flow.query["item"]
    if len(flow._renames) != 0:
        t = []
        for k in keys:
            if k in dict(flow._renames):
                t.append(dict(flow._renames)[k])
            else:
                t.append(k)
        keys = t
    return keys


def no_sql_action(name, keys, fact, query={}):
    """
    # get -> 'cpu' : '%cpu_status' => cpu = 34.3%
        * watch task

    # func -> 'id' : 'id()' => id = 1
        * load plugin

    # py -> '?isAdmin' : '"admin_" in name'
        * eval python
    """
    if keys[0] == "get":
        return call_watch(keys[1])
    elif keys[0] == "func":
        return call_plugin(keys[1][0], query.copy(), keys[1][1])
    elif keys[0] == "py":
        return eval(keys[1], query.copy())
    return ""


def dump_(flow, fact):
    if flow.table is None:
        body_res = dict()
        for k, v in flow.body:
            if isinstance(v, Json_flow):
                body_res[k] = dump_(v, fact)
            else:
                body_res[k] = no_sql_action(k, v, fact)
        return body_res
    new_keys = get_new_keys(flow, fact)
    sql_res = list(fact.commit(flow.script))
    query_res = []
    for r in sql_res:
        query_res.append(dict(zip(new_keys, r)))

    if flow.type == "object":
        q_res = query_res[:1]
    else:
        q_res = query_res

    res = []
    for r in q_res:
        for k, value in flow.body:
            if isinstance(value, Json_flow):
                v = copy.deepcopy(value)
                if v.table:
                    for_keys = fact.foreign_key(flow.table, v.table)
                    if len(for_keys) is 0:
                        r[k] = "NOT FOUND"
                        continue
                    for key, val in for_keys:
                        if r[key] is None:
                            r[k] = "NOT FOUND"
                            break
                        if r[key]:
                            v.query["where"].append(f"{val}={r[key]}")
                if k not in r:
                    r[k] = dump_(v, fact)
            else:
                r[k] = no_sql_action(k, value, fact, r)
        res.append(r)
    if flow.type != "object":
        return res
    else:
        return res[0] if len(res) == 1 else []


class executor(object):
    def __init__(self, json_string, query_factory):
        self.flow = json_parse(json_string)
        self.factory = query_factory

    def dump(self):
        return dump_(self.flow, self.factory)
