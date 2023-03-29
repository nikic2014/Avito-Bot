import sqlalchemy as db
from sqlalchemy import Column, Text, Integer, Table, select, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import host, user, password, db_name

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


print("Подключение к базе прошло успешно")