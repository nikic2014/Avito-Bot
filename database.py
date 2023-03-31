import sqlalchemy as db
from sqlalchemy import Column, Text, Integer, Table, select, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from MyLogging import database_loger
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
    link = Column(Text, primary_key=True)

database_loger.info("Классы в базе данных успешно созданы")

def get_cars(req, lock):
    database_loger.info("Зашли в функцию иформации о машинах")
    lock.acquire()
    database_loger.info("Заблокировали функцию")
    engine = db.create_engine(
        f"postgresql://{user}:{password}@localhost/{db_name}",
        pool_pre_ping=True)
    conaction = engine.connect()

    database_loger.info("Подключились к базе данных")

    BaseClass.metadata.create_all(engine)

    result = conaction.execute(req).fetchall()
    conaction.close()
    database_loger.info(f'Запрос: {req}')
    database_loger.info(f'Результат запроса: {result}')
    database_loger.info("Подключение к базе данных закрыто")

    lock.release()
    database_loger.info('Разблокировали функцию')
    database_loger.info("\n------------------------------------------------\n")

    return result


def get_images(req, lock):
    database_loger.info("Зашли в функцию иформации о картинках")

    lock.acquire()
    database_loger.info("Заблокировали функцию")

    engine = db.create_engine(
        f"postgresql://{user}:{password}@localhost/{db_name}",
        pool_pre_ping=True)
    conaction = engine.connect()
    database_loger.info("Подключились к базе данных")

    BaseClass.metadata.create_all(engine)

    result = conaction.execute(req).fetchall()
    conaction.close()
    database_loger.info(f'Запрос: {req}')
    database_loger.info(f'Результат запроса: {result}')
    database_loger.info("Подключение к базе данных закрыто")

    lock.release()
    database_loger.info('Разблокировали функцию')
    database_loger.info("\n------------------------------------------------\n")

    return result


def set_car(req, lock):
    database_loger.info("Зашли в функцию добавления и удаления машин")

    lock.acquire()
    database_loger.info("Заблокировали функцию")

    engine = db.create_engine(
        f"postgresql://{user}:{password}@localhost/{db_name}",
        pool_pre_ping=True)
    conaction = engine.connect()
    BaseClass.metadata.create_all(engine)
    database_loger.info("Подключились к базе данных")

    result = conaction.execute(req)
    conaction.commit()
    conaction.close()
    database_loger.info(f'Запрос: {req}')
    database_loger.info(f'Результат запроса: {result}')
    database_loger.info("Подключение к базе данных закрыто")

    lock.release()
    database_loger.info("Разблокировали функцию")
    database_loger.info("\n------------------------------------------------\n")

    return result


def set_image(req, lock):
    lock.acquire()
    database_loger.info("Заблокировали функцию")

    engine = db.create_engine(
        f"postgresql://{user}:{password}@localhost/{db_name}",
        pool_pre_ping=True)
    conaction = engine.connect()
    BaseClass.metadata.create_all(engine)
    database_loger.info("Подключились к базе данных")

    result = conaction.execute(req)
    conaction.commit()
    conaction.close()
    database_loger.info(f'Запрос: {req}')
    database_loger.info(f'Результат запроса: {result}')
    database_loger.info("Подключение к базе данных закрыто")

    lock.release()
    database_loger.info("Разблокировали функцию")
    database_loger.info("\n------------------------------------------------\n")

    return result
