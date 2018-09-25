class Json_flow(object):
    def __init__(self, type="object"):
        self.type = type
        self.query = {"where":[],"item":[]}
        self._renames, self.body = [], []
        self.table = None

    @property
    def is_query_all_item(self):
        return len(self.query["item"]) == 0 or "*" in self.query["item"]

    @property
    def is_none_condition(self):
        return len(self.query["where"]) == 0

    @property
    def script(self):
        items, wheres = self.query["item"], self.query["where"]
        item_sql = "*" if self.is_query_all_item else ",".join(items)
        where_sql = "" if self.is_none_condition else ("WHERE " + " AND ".join(wheres))
        return f"SELECT {item_sql} FROM {self.table} {where_sql}"
