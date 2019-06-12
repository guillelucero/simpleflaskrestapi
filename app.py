#!/usr/bin/python3


from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from tinydb import TinyDB, Query
from tinydb.operations import delete
from tinydb.queries import where
import datetime;

db = TinyDB('./db.json')
Log = Query()

app = Flask(__name__)
api = Api(app)

# full logs
class Logs(Resource):

    def get(self):
        result = jsonify(db.search(Log))
        return result

# full logs operation by source
class Source(Resource):

    def get(self):
        result = jsonify(db.search(Log))
        return result

    def get(self, source_id):
        result = jsonify(db.search(Log.source.source_id == source_id))
        return result

    def post(self, source_id):
        print(request.json)
        source = {'source_id': source_id, 'timestamp': datetime.datetime.now().timestamp()}
        log = {'source': source, 'log': request.json}
        db.insert(log)
        return {'status': 'success'}

    def delete(self, source_id):
        db.update(delete('log'), Log.source.source_id == source_id)
        db.update(delete('source'), Log.source.source_id == source_id)
        return {'status': 'success'}


api.add_resource(Source, '/source/<source_id>')
api.add_resource(Logs, '/logs/')
#TODO
# /timestamp/
# /custom_filter - user could need to filer logs with specific pattern.
# /logs - delete method.


if __name__ == '__main__':
    app.run(host='0.0.0.0')