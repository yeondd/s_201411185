use myDB
show dbs
show tables
db.myCol.insert({"Persons":[{"id":"201411185", "�̸�":"sy"},{"id":"201411190", "�̸�":"sb"}]})
db.myCol.find({ "Persons.�̸�": "sy" })