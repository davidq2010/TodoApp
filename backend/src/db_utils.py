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
        """
        Creates an entry for a SchemaObject and inserts it into the database.

        Parameters:
            schema_obj (SchemaObject): Object to create and insert a db entry for

        Returns:
            dict (serialized) form of the newly-inserted entry
        """
        coll_type = type(schema_obj).__name__
        if DEBUG:
            print("In DBHandler.create, serializing obj of type {}".format(coll_type))

        # Serialize schema_obj (without _id) into dict, then insert into db.
        dictified_obj = self._no_id_serializer_map[coll_type].dump(schema_obj)
        self.db[coll_type].insert_one(dictified_obj) # will add _id since not present

        if DEBUG: print("DB obj:", dictified_obj)

        #TODO: Have required and non-required set

        # Deserialize the dict that was just inserted into the db; now has _id
        db_obj = self._general_serializer_map[coll_type].load(dictified_obj)

        # Re-serialize the object (w/_id) that was inserted into db to return
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
        # find_one includes _id in the returned dict
        db_resp = self.db[coll_type.value].find_one({'_id': id})
        # Serialize the returned db dict into dict that we know can pass through
        # the Schema. TODO: Is this necessary?
        serialized_db_resp = self._general_serializer_map[coll_type.value].dump(db_resp)
        if DEBUG: print("Found task. Serialized to:", serialized_db_resp)
        return serialized_db_resp

    def delete(self, coll_type: CollectionType, id: bson.ObjectId):
        db_resp = self.db[coll_type.value].delete_one({'_id': id})
        return db_resp.deleted_count

    def update(self, coll_type: CollectionType, id: bson.ObjectId,
            schema_obj: SchemaObject):
        # Filter the db using _id, the replacement dict should not have _id, but
        # should have all other attributes (hence _no_id_serializer_map)
        repl_dict = self._no_id_serializer_map[coll_type.value].dump(schema_obj)
        db_resp = self.db[coll_type.value].replace_one({'_id': id}, repl_dict)
        # TODO: Should we return a dict w/_id (this one doesn't)
        return db_resp.matched_count, repl_dict
