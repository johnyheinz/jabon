from sqlalchemy import create_engine, select, Table, Column, Integer, String, ForeignKey, MetaData, inspect
from sqlalchemy.sql import select
import os

engstring = os.environ['ENGINE_STRING']
engine = create_engine(f'{engstring}', echo=True)
meta = MetaData(engine)
conn = engine.connect()

if (not(inspect(engine).has_table('JABON_table'))):
    userinfotable = Table('JABON_table', meta,
    Column('vk_id', Integer, primary_key=True, nullable=False),
    Column('name', String(100), nullable=False),
    Column('city', String(100), nullable=False),
    Column('private', String(5))
    )
    meta.create_all(engine)
else: userinfotable = Table('JABON_table', meta, autoload=True)

async def refreshdb(tupledb):
    try:
        insert_query = userinfotable.insert().values(vk_id = tupledb[0], name = tupledb[1], city = tupledb[2], private = tupledb[3])
        conn.execute(insert_query)
    except:
        update_query = userinfotable.update().where(userinfotable.c.vk_id == tupledb[0]).values(name = tupledb[1], city = tupledb[2], private = tupledb[3])
        conn.execute(update_query)

async def updatecity(addtuple):
    update_query = userinfotable.update().where(userinfotable.c.vk_id == addtuple[0]).values(city = addtuple[1])
    conn.execute(update_query)

async def giveinfodb(vk_id_number):
    userselect = select(userinfotable).where(userinfotable.c.vk_id == vk_id_number)
    usertuple = conn.execute(userselect)
    return usertuple.fetchone()

    