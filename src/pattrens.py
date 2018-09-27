import re


__all__ = ("pattrens",)
pattrens = {
    "db_rename": re.compile(r"^(\w+)\.(\w+)$"),
    "function": re.compile(r"^(\w+)\((.+)\)$"),
    "db_other": re.compile(r"^(\w+)\.{3}$"),
    "type_object": re.compile(r"^\{\w+\}$"),
    "type_array": re.compile(r"^\[\w+\]$")
}
