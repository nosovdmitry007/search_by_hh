from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///HH_search_orm.sqlite', echo=True)

Base = declarative_base()

Vacancyskil = Table('vacancyskil', Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('vacancy_id', Integer, ForeignKey('vacancy.id')),
                     Column('skil_id', Integer, ForeignKey('skills_table.id'))
                     )


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(String)
    about = Column(String)
    link = Column(String, unique=True)

    children = relationship("Skills_table", secondary=Vacancyskil, back_populates="parents")

    def __init__(self, name,salary,about,link):
        self.name = name
        self.salary = salary
        self.about = about
        self.link = link


    def __str__(self):
        return f'{self.id}, {self.name}, {self.salary}, {self.about}, {self.link}'

class Params(Base):
    __tablename__ = 'params'
    id = Column(Integer, primary_key=True)
    name_search = Column(String)
    where_search = Column(String)

    def __init__(self, name_search, where_search):
        self.name_search = name_search
        self.where_search = where_search
    def __str__(self):
        return f'{self.id}, {self.name_search}, {self.where_search}'
class Skills_table(Base):
    __tablename__ = 'skills_table'
    id = Column(Integer, primary_key=True)
    skil = Column(String, unique=True, nullable=True)
    how_many_skil = Column(Integer)
    parents = relationship("Vacancy", secondary=Vacancyskil, back_populates="children")

    def __init__(self, skil, how_many_skil):
        self.skil = skil
        self.how_many_skil = how_many_skil
    def __str__(self):
        return f'{self.id}, {self.skil}, {self.how_many_skil}'


# Создание таблицы
Base.metadata.create_all(engine)

