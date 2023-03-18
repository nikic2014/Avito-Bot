import sqlalchemy as db
from sqlalchemy import Column, Text, Integer, Table, select, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from config import host, user, password, db_name
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine(f"postgresql://{user}:{password}@localhost/{db_name}",
                          pool_pre_ping=True)
conaction = engine.connect()
metadata = db.MetaData()
BaseClass = declarative_base()

class Cars_ads(BaseClass):
    __tablename__ = 'Cars'

    link = Column(Text, primary_key=True, unique=True)
    title = Column(Text)
    price = Column(Integer)
    description = Column(Text)

class Images_cars(BaseClass):
    __tablename__ = 'Images_car'

    fk_link = Column(Text, ForeignKey('Cars.link'))
    link = Column(Text,primary_key=True)

BaseClass.metadata.create_all(engine)

ins = insert(Images_cars).values(["a","b"])
compiled = ins.compile()
print(compiled.params)
result = conaction.execute(ins)
conaction.commit()




# metadata.create_all(engine)
#
#
# Session = sessionmaker(bind = engine)
# session = Session()
#
# ins = images_cars.insert().values(fk_link = 'Ravi', link = 'Kapoor')
# result = conaction.execute(ins)
#
# session.add()
# session.commit()
#
# s = images_cars.select()
# result = conaction.execute(s)
# print(result.fetchall())
#
# s = select(images_cars)
# result = conaction.execute(s)
# print(result.fetchall())
#


print("Подключение к базе прошло успешно")