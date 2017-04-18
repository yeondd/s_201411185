import pymongo
from pymongo import MongoClient

client = MongoClient()
db=client.myDB


_id=201411185
_name='sy'
_age=23
_country='ko'

db.myPyCol.insert_one({
    "id": _id,
    "name": _name,
    "age": _age,
    "country": _country
})

client = MongoClient('localhost:27017')
db=client.myDB
results = db.myCol.find()
for r in results:
  print r['Persons']