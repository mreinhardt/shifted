from collections import defaultdict
import json


class KeyColumnValueStore(object):
    def __init__(self, path=None):
        # even if path doesn't exist, will still save there
        self.path = path

        # load from path if possible
        if path is not None:
            try:
                with open(path, 'r') as disk_store:
                    self._store = defaultdict(
                        dict, json.loads(disk_store.read()))
            except IOError as e:
                self._store = defaultdict(dict)
        else:
            self._store = defaultdict(dict)

    def set(self, key, col, val):
        """ sets the value at the given key/column """
        key_dict = self._store[key]
        key_dict[col] = val
        self._save()

    def get(self, key, col):
        """ return the value at the specified key/column """
        if key in self._store:
            if col in self._store[key]:
                return self._store[key][col]
        return None

    def get_key(self, key):
        """ returns a sorted list of column/value tuples """
        if key in self._store:
            return sorted(self._store[key].items())
        return []

    def get_keys(self):
        """ returns a set containing all of the keys in the store """
        return set(self._store.keys())

    def delete(self, key, col):
        """ removes a column/value from the given key """
        if key in self._store:
            if col in self._store[key]:
                del self._store[key][col]
        self._save()

    def delete_key(self, key):
        """ removes all data associated with the given key """
        if key in self._store:
            del self._store[key]
        self._save()

    def get_slice(self, key, start, stop):
        """
        returns a sorted list of column/value tuples where the column
        values are between the start and stop values, inclusive of the
        start and stop values. Start and/or stop can be None values,
        leaving the slice open ended in that direction
        """
        full_key = self.get_key(key)
        sliced_key = []
        for k in full_key:
            if ((start is None or min(k[0], start) == start) and
                (stop is None or max(k[0], stop) == stop)):
                sliced_key.append(k)
        return sliced_key

    def _save(self):
        """ save store to disk at path """
        if self.path is not None:
            with open(self.path, 'w') as disk_store:
                disk_store.write(json.dumps(self._store))
