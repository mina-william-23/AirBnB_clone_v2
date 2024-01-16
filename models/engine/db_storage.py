#!/usr/bin/python3
"""DBStorage Class"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from models.base_model import Base
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ DBStorage constructor """
        try:
            self.__config = {
                'env': os.getenv('HBNB_ENV'),
                'dialect': 'mysql',
                'driver': 'mysqldb',
                'host': os.getenv('HBNB_MYSQL_HOST'),
                'user': os.getenv('HBNB_MYSQL_USER'),
                'pwd': os.getenv('HBNB_MYSQL_PWD'),
                'db': os.getenv('HBNB_MYSQL_DB'),
            }
            self.__engine = create_engine('{}+{}://{}:{}@{}/{}'.format(
                self.__config['dialect'],
                self.__config['driver'],
                self.__config['user'],
                self.__config['pwd'],
                self.__config['host'],
                self.__config['db']
            ), pool_pre_ping=True)
        except Exception:
            pass
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Return dictionary of objects
        """
        dbResult = {}
        validClass = {'User': User, 'Place': Place,
                      'State': State, 'City': City,
                      'Amenity': Amenity, 'Review': Review}
        if cls is None:
            for val in validClass.values():
                query = self.__session.query(val)
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    dbResult[key] = obj

        elif cls in validClass:
            query = self.__session.query(validClass[cls])
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dbResult[key] = obj

        return dbResult

    def new(self, obj):
        """Add object to database session
        """
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from database
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
