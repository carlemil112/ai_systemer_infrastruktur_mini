from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float, func

engine = create_engine('sqlite:///mydatabase.db', echo=True)
meta = MetaData()

# ---------- TABLE DEFINITIONS ----------
users = Table(
    'users', 
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)

things = Table(
    'things',
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('users.id'))
)

# ---------- DROP + CREATE ----------
things.drop(engine, checkfirst=True)
users.drop(engine, checkfirst=True)
meta.create_all(engine)

conn = engine.connect()

# ---------- INSERT DATA (THIS IS WHAT YOU WERE MISSING) ----------
insert_user = users.insert().values([
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 35},
    {'name': 'Diana', 'age': 28},
    {'name': 'Ethan', 'age': 40}
])

insert_things = things.insert().values([
    {'owner': 1, 'description': 'Laptop', 'value': 1200.00},
    {'owner': 2, 'description': 'Smartphone', 'value': 800.00},
    {'owner': 3, 'description': 'Tablet', 'value': 600.00},
    {'owner': 4, 'description': 'Monitor', 'value': 300.00},
    {'owner': 5, 'description': 'Headphones', 'value': 150.00}
])

conn.execute(insert_user)
conn.execute(insert_things)
conn.commit()     

group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.value)).group_by(things.c.owner)
result = conn.execute(group_by_statement)

for row in result.fetchall():
    print(row)