
# please see instructions.txt for details on what to do

class KeyColumnValueStore(object):

    def set(self, key, col, val):
        """ sets the value at the given key/column """

    def get(self, key, col):
        """ return the value at the specified key/column """

    def get_key(self, key):
        """ returns a sorted list of column/value tuples """

    def get_keys(self):
        """ returns a set containing all of the keys in the store """

    def delete(self, key, col):
        """ removes a column/value from the given key """

    def delete_key(self, key):
        """ removes all data associated with the given key """