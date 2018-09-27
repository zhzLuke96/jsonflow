from .parser import json_parse
from .flow import Json_flow

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
    if keys[0] == "get":
        return fact.variable.get(keys[1], lambda x=0: query.get(keys[1], ""))()
    elif keys[0] == "func":
        return None
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
        for k, v in flow.body:
            if isinstance(v, Json_flow):
                if v.table:
                    for key, val in fact.foreign_key(flow.table, v.table):
                        if r[key]:
                            v.query["where"].append(f"{val}={r[key]}")
                r[k] = dump_(v, fact)
            else:
                r[k] = no_sql_action(k, v, fact, r)
        res.append(r)
    if flow.type != "object":
        return res
    else:
        return res[0] if len(res) == 1 else []


def flow_dump(flow, query_factory):
    if flow.table is None:
        body_res = dict()
        for k, v in flow.body:
            if isinstance(v, Json_flow):
                body_res[k] = flow_dump(v, query_factory)
            else:
                body_res[k] = v
        return body_res
    query_result = list(query_factory.commit(flow.script))
    if flow.is_query_all_item:
        keys = query_factory.get_keys(flow.table)
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

    if flow.type == "object":
        return dict(zip(keys, query_result[0]) + body_res.items())
    else:
        # type := array
        res = []
        for r in query_result:
            res.append(dict(zip(keys, r)))
        return res


class executor(object):
    def __init__(self, json_string, query_factory):
        self.flow = json_parse(json_string)
        self.factory = query_factory

    def dump(self):
        return dump_(self.flow, self.factory)
