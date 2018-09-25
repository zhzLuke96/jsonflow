from .parser import json_parse
from .flow import Json_flow

__all__ = ("executor",)


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
        return flow_dump(self.flow, self.factory)
