#!/usr/bin/env python
import argparse
import json

from flask import Flask, jsonify, abort, request, make_response

from src.KeyColumnValueStore import KeyColumnValueStore


kcvs = KeyColumnValueStore()
api = Flask(__name__)


@api.route('/')
def index():
    return 'datastore: {0}'.format(repr(kcvs.path))


@api.route('/api/')
def api_routes():
    return """/api/keys/ (GET);
/api/key/[key]/ (GET, DELETE);
/api/key/[key]/col/[col]/ (GET, POST, DELETE);
/api/slice/key/[key]/?start=[start]&stop=[stop] (GET);
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
    if request.method == 'POST':
        raw_data = request.get_data()
        if raw_data:
            value = json.loads(raw_data).get('value', None)
            kcvs.set(key, col, value)
        else:
            return make_response(
                jsonify({'error': 'No data received in POST'}), 400)
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
