class Json_flow(object):
    def __init__(self, type="object"):
        self.type = type
        self._dbs, self._renames, self.body = [], [], []
        self.table = None
