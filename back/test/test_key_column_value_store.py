import os
import random
import string
import unittest

from src.KeyColumnValueStore import KeyColumnValueStore


class TestKeyColumnValueStore(unittest.TestCase):

    def setUp(self):
        # save test store to disk
        self._path = '/tmp/_test_kcvs'
        kcvs = KeyColumnValueStore(path=self._path)
        kcvs.set('z', 'zz', 41)
        kcvs.set('z', 'yy', 42)
        kcvs.set('y', 'xx', 68)
        kcvs.set('x', 'ww', 67)

        self.kcvs = KeyColumnValueStore()

    def tearDown(self):
        os.remove(self._path)

    def test_get_when_empty(self):
        self.assertIsNone(self.kcvs.get('a', 'aa'))

    def test_set_and_get(self):
        self.kcvs.set('a', 'aa', 1)
        self.assertEqual(self.kcvs.get('a', 'aa'), 1)

    def test_set_overwrite(self):
        self.kcvs.set('a', 'aa', 1)
        self.assertEqual(self.kcvs.get('a', 'aa'), 1)
        self.kcvs.set('a', 'aa', 2)
        self.assertEqual(self.kcvs.get('a', 'aa'), 2)

    def test_get_key_when_empty(self):
        self.assertEqual(self.kcvs.get_key('a'), [])

    def test_get_key(self):
        self.kcvs.set('a', 'aa', 1)
        self.assertEqual(self.kcvs.get_key('a'), [('aa', 1)])

    def test_get_key_sorted(self):
        self.kcvs.set('a', 'ba', 0)
        self.kcvs.set('a', 'aa', 2)
        self.kcvs.set('a', 'ab', 1)
        self.assertEqual(
            self.kcvs.get_key('a'), [('aa', 2), ('ab', 1), ('ba', 0)])

    def test_get_keys_when_empty(self):
        self.assertEqual(self.kcvs.get_keys(), set([]))

    def test_get_keys(self):
        self.kcvs.set('a', 'b', 0)
        self.kcvs.set('b', 'c', 2)
        self.kcvs.set('c', 'd', 1)
        self.assertEqual(self.kcvs.get_keys(), set(['a', 'b', 'c']))

    def test_delete_when_empty(self):
        self.kcvs.delete('a', 'b')  # shouldn't raise exception

    def test_delete(self):
        self.kcvs.set('a', 'b', 0)
        self.kcvs.set('a', 'a', 2)
        self.kcvs.set('c', 'd', 1)
        self.kcvs.delete('a', 'b')
        self.assertIsNone(self.kcvs.get('a', 'b'))
        self.assertEqual(self.kcvs.get('a', 'a'), 2)
        self.assertEqual(self.kcvs.get_keys(), set(['a', 'c']))

    def test_delete_key_when_empty(self):
        self.kcvs.delete_key('a')  # shouldn't raise exception

    def test_delete_key(self):
        self.kcvs.set('a', 'b', 0)
        self.kcvs.set('a', 'a', 2)
        self.kcvs.set('c', 'd', 1)
        self.kcvs.delete_key('a')
        self.assertIsNone(self.kcvs.get('a', 'b'))
        self.assertIsNone(self.kcvs.get('a', 'a'))
        self.assertEqual(self.kcvs.get_keys(), set(['c']))

    def test_get_slice_when_empty(self):
        self.assertEqual(self.kcvs.get_slice('a', 'ac', 'af'), [])

    def test_get_slice(self):
        self.kcvs.set('a', 'aa', 6)
        self.kcvs.set('a', 'ab', 2)
        self.kcvs.set('a', 'ac', 4)
        self.kcvs.set('a', 'ad', 3)
        self.kcvs.set('a', 'ae', 7)
        self.kcvs.set('a', 'af', 9)
        self.kcvs.set('a', 'ag', 8)
        self.assertEqual(
            self.kcvs.get_slice('a', 'ac', 'ae'),
            [('ac', 4), ('ad', 3), ('ae', 7)])
        self.assertEqual(
            self.kcvs.get_slice('a', 'ae', None),
            [('ae', 7), ('af', 9), ('ag', 8)])
        self.assertEqual(
            self.kcvs.get_slice('a', None, 'ac'),
            [('aa', 6), ('ab', 2), ('ac', 4)])

    def test_get_slice_between_cols(self):
        self.kcvs.set('a', 'aa', 6)
        self.kcvs.set('a', 'ac', 2)
        self.kcvs.set('a', 'ae', 4)
        self.kcvs.set('a', 'ag', 3)
        self.kcvs.set('a', 'ai', 7)
        self.kcvs.set('a', 'ak', 9)
        self.kcvs.set('a', 'am', 8)
        self.assertEqual(
            self.kcvs.get_slice('a', 'ad', 'aj'),
            [('ae', 4), ('ag', 3), ('ai', 7)])
        self.assertEqual(
            self.kcvs.get_slice('a', 'ah', None),
            [('ai', 7), ('ak', 9), ('am', 8)])
        self.assertEqual(
            self.kcvs.get_slice('a', None, 'af'),
            [('aa', 6), ('ac', 2), ('ae', 4)])

    def test_load_nonexistant_file(self):
        _filename = '/tmp/' + ''.join(
            [random.choice(string.ascii_letters) for _ in xrange(15)])
        self.kcvs = KeyColumnValueStore(path=_filename)

    def test_load_nonexistant_file_and_saves(self):
        _filename = '/tmp/' + ''.join(
            [random.choice(string.ascii_letters) for _ in xrange(15)])
        self.kcvs = KeyColumnValueStore(path=_filename)
        self.kcvs.set('a', 'zz', 12)
        self.kcvs = KeyColumnValueStore()
        self.assertIsNone(self.kcvs.get('a', 'zz'))
        self.kcvs = KeyColumnValueStore(path=_filename)
        self.assertEqual(self.kcvs.get('a', 'zz'), 12)
        os.remove(_filename)

    def test_load_existing_file(self):
        self.kcvs = KeyColumnValueStore(path=self._path)
        self.assertEqual(self.kcvs.get('z', 'yy'), 42)

    def test_delete_key_from_existing_file(self):
        self.kcvs = KeyColumnValueStore(path=self._path)
        self.assertEqual(self.kcvs.get('z', 'yy'), 42)
        self.kcvs.delete_key('z')
        self.kcvs = KeyColumnValueStore()
        self.assertEqual(self.kcvs.get_key('y'), [])
        self.assertEqual(self.kcvs.get_key('z'), [])
        self.kcvs = KeyColumnValueStore(path=self._path)
        self.assertEqual(self.kcvs.get_key('y'), [('xx', 68)])
        self.assertEqual(self.kcvs.get_key('z'), [])


if __name__ == '__main__':
    unittest.main()
