from pymongo import MongoClient
from typing import Dict
from .models.models import SchemaObject, TaskSchema, WhoAmISchema, Task, WhoAmI
from enum import Enum
from flask import jsonify
from marshmallow import fields
import bson

DEBUG = True

class CollectionType(Enum):
    TASK = Task.__name__
    WHOAMI = WhoAmI.__name__

class MongoDBHandler:
    def __init__(self, url: str):
        self.db = MongoClient(url)["StressorDB"]
        # _id isn't in the Schema, it's just Mongo-specific, so exclude it when
        # serializing.
        # Will have lots of fields set to None
        self._no_id_serializer_map = {
                Task.__name__: TaskSchema(exclude=['_id'], unknown='RAISE'),
                WhoAmI.__name__: WhoAmISchema()}
        self._general_serializer_map = {
                Task.__name__: TaskSchema(unknown='RAISE'),
                WhoAmI.__name__: WhoAmISchema()}

    def create(self, schema_obj: SchemaObject):
        # route controller will load serialized request.data into SchemaObject
        # using correct Schema.
        # We call insert(SchemaObject) then return a json response with a payload
        # containing the serialized object that was inserted (will have
        # createTime now). Will require a json.dumps I think.
        # Serialize schema_obj into dict, then insert into db.
        coll_type = type(schema_obj).__name__
        if DEBUG:
            print("In DBHandler.create, serializing obj of type {}".format(coll_type))
        dictified_obj = self._no_id_serializer_map[coll_type].dump(schema_obj)
        self.db[coll_type].insert_one(dictified_obj) # adds _id if not present
        if DEBUG: print("DB obj:", dictified_obj)
        #TODO: Have required an non-required set
        db_obj = self._general_serializer_map[coll_type].load(dictified_obj)
        serialized_db_obj = self._general_serializer_map[coll_type].dump(db_obj)
        return serialized_db_obj

    def find_all(self, coll_type: CollectionType):
        docs = self.db[coll_type.value].find({})
        # docs has json serialized documents from a collection
        # Iterate over them and serialize again according to schema.
        # In app route, return json response w/payload containing this
        # serialized object. Will require a json.dumps I think.
        db_resp = [self._general_serializer_map[coll_type.value].dump(doc)
                for doc in docs]
        if DEBUG:
            for resp in db_resp:
                print(resp)

        return jsonify(db_resp)

    def find_one(self, coll_type: CollectionType, id: bson.ObjectId):
        db_resp = self.db[coll_type.value].find_one({'_id': id})
        serialized_db_resp = self._general_serializer_map[coll_type.value].dump(db_resp)
        if DEBUG: print("Found task. Serialized to:", serialized_db_resp)
        return serialized_db_resp

    def delete(self, coll_type: CollectionType, id: bson.ObjectId):
        db_resp = self.db[coll_type.value].delete_one({'_id': id})
        # In app route (task/<id>) return json response that's sth like
        # ({'ok': True, 'message': 'record deleted'}, 200) if the delete_count
        # is 1.
        return db_resp.deleted_count

    def update(self, coll_type: CollectionType, id: bson.ObjectId,
            schema_obj: SchemaObject):
        # Cannot replace _id of a db document, hence _no_id_serializer_map
        repl_dict = self._no_id_serializer_map[coll_type.value].dump(schema_obj)
        db_resp = self.db[coll_type.value].replace_one({'_id': id}, repl_dict)
        return db_resp.matched_count, repl_dict
