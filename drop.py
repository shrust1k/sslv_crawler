import sqlalchemy
conn = sqlalchemy.create_engine("sqlite:///db.db")
db = conn.connect()

db.execute(sqlalchemy.text("DROP TABLE ads"))
db.commit()