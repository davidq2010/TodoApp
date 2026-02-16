from marshmallow import Schema, fields, post_load
import time
import bson

# So in both sql and mongo, we need to (de)serialize the json request/response
# objects into regular class objects. The difference is with sqlalch, the
# regular objects extend db.model while with mongo, we don't need to extend
# anything. Then we can create schemas that extend marshmallow Schema to
# serialize the regular objects.

# https://marshmallow.readthedocs.io/en/stable/_modules/marshmallow/fields.html
class ObjectId(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return bson.ObjectId(value)
        except (TypeError, bson.errors.InvalidId):
            raise ValidationError(_('Invalid ObjectId.'))

class SchemaObject:
    def __init__(self, _id: bson.ObjectId=None, created_at: int=None):
        self.created_at = created_at if created_at else int(time.time())
        self._id = _id

class Task(SchemaObject):
    def __init__(self, description: str, priority: int, _id: bson.ObjectId=None,
            created_at: int=None, detail: str=None, work_hr_est: float=None):
        super().__init__(_id, created_at)
        self.description = description
        self.priority = priority
        self.detail = detail
        self.work_hr_est = work_hr_est

class WhoAmI(SchemaObject):
    def __init__(self, whoami: str):
        super().__init__()
        self.whoami = whoami

class TaskSchema(Schema):
    # required => needed for deserialization into Task object.
    description = fields.Str(required=True)
    priority = fields.Int(required=True)
    created_at = fields.Int()
    _id = ObjectId()
    detail = fields.Str(allow_none=True) # Otherwise validation error is thrown
    work_hr_est = fields.Float(allow_none=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)

class WhoAmISchema(Schema):
    id = fields.Int()
    whoami = fields.Str()

    @post_load
    def make_whoami(self, data, **kwargs):
        return WhoAmI(**data)
