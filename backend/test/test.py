from models import *
import bson

create_req = {'description': 'eat', 'priority': 1}
create_schema = TaskSchema(exclude=['_id', 'created_at'])
create_obj = create_schema.load(create_req)

db_create_schema = TaskSchema(exclude=['_id'])
db_create_dict = db_create_schema.dump(create_obj)
print("Pre-insert", db_create_dict)
# after inserting into db
db_create_dict['_id'] = bson.ObjectId('507f1f77bcf86cd799439011')
print("Post-insert", db_create_dict)

gen_db_schema = TaskSchema()
valid_resp_obj = gen_db_schema.load(db_create_dict)
db_resp = gen_db_schema.dump(valid_resp_obj)
print(db_resp)
