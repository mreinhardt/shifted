#!/usr/bin/env python
import argparse

from flask import Flask, jsonify, abort, request

from src.KeyColumnValueStore import KeyColumnValueStore


kcvs = KeyColumnValueStore()
api = Flask(__name__)


@api.route('/')
def index():
    return 'datastore: {0}'.format(repr(kcvs.path))


@api.route('/api/')
def api_routes():
    return """/api/keys/ (GET)
/api/key/<kev>/ (GET, DELETE)
/api/key/<key>/col/<col>/ (GET, POST, DELETE)
/api/slice/key/<key>/?start=<start>&stop=<stop> (GET)
"""


@api.route('/api/keys/', methods=['GET'])
def get_keys():
    return jsonify({'keys': list(kcvs.get_keys())})


@api.route('/api/key/<key>/', methods=['GET', 'DELETE'])
def key(key):
    if request.method == 'DELETE':
        kcvs.delete_key(key)
        cols = []
    elif request.method == 'GET':
        cols = kcvs.get_key(key)
    else:
        pass

    return jsonify({
        'key': key,
        'cols': cols
    })


@api.route('/api/key/<key>/col/<col>/', methods=['GET', 'POST', 'DELETE'])
def key_col(key, col):
    if request.method == 'POST' and request.json and 'value' in request.json:
        kcvs.set(key, col, request.json['value'])
        value = request.json['value']
    elif request.method == 'GET':
        value = kcvs.get(key, col)
    elif request.method == 'DELETE':
        kcvs.delete(key, col)
        value = None
    else:
        pass

    return jsonify({
        'key': key,
        'col': col,
        'value': value
    })


@api.route('/api/slice/key/<key>/', methods=['GET'])
def slice(key):
    start = request.args.get('start', None)
    stop = request.args.get('stop', None)

    return jsonify({
        'key': key,
        'start': start,
        'stop': stop,
        'cols': kcvs.get_slice(key, start, stop)
    })


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='KeyColumnValueStore API',
        usage='./api.py [options]')
    argparser.add_argument('-d', '--datastore',
        help='path to existing datastore')

    args = argparser.parse_args()
    if args.datastore:
        kcvs = KeyColumnValueStore(path=args.datastore)

    api.run(debug=True)
