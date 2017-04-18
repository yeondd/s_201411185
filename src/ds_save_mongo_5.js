use myDB
show dbs
show tables
db.myCol.insert({"Persons":[{"id":"201411185", "이름":"sy"},{"id":"201411190", "이름":"sb"}]})
db.myCol.find({ "Persons.이름": "sy" })