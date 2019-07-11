import DBaction

db = DBaction.DBac()
db.__init__()
db.insert("BadWords",'铁憨憨')
rows = db.select("BadWords")
print(rows)