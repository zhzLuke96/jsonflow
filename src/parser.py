import json
from .pattrens import pattrens
from .flow import Json_flow

__all__ = ("json_parse",)


def parse_expression(key, val):
    if key[0] == "!":
        return ("db_where", f"{key[1:]} {val}")
    elif key == "...":
        return ("db_table", f"{val}")
    elif key[0] == "?":
        return ("py", val)
    elif val[0] == "%":
        return ("get", val[1:])
    elif pattrens["db_rename"].match(val):
        m = pattrens["db_rename"].match(val)
        return ("rename", m.group(1), m.group(2))
    elif pattrens["function"].match(val):
        m = pattrens["function"].match(val)
        return ("func", m.group(1), m.group(2))
    elif pattrens["db_other"].match(val):
        m = pattrens["db_other"].match(val)
        return ("other", m.group(1))
    else:
        # holder
        return ("ERROR", val)


def json_parse(json_string):
    _j = json.loads(json_string)

    def parse_obj(name, obj):
        if isinstance(obj, dict):
            type_name = "object"
            if pattrens["type_array"].match(name):
                type_name = "array"
            flow = Json_flow(type_name)
            for key, val in obj.items():
                p = parse_obj(key, val)
                if isinstance(p, Json_flow):
                    flow.body.append((key[1:-1], p))
                elif "db" in p[0]:
                    if "table" in p[0]:
                        flow.table = p[1]
                        flow.query["item"].append("*")
                        continue
                    flow.query["where"].append(p[1])
                elif p[0] == "rename":
                    flow.table = p[1]
                    flow.query["item"].append(p[2])
                    flow._renames.append((p[2],key))
                else:
                    flow.body.append(p)
            return flow
        else:
            return parse_expression(name, obj)

    return parse_obj("root", _j)
