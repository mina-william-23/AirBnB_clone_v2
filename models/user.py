#!/usr/bin/python3
"""This module defines a class User"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ User Class subclass of BaseModel """
    __tablename__ = "users"
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", passive_deletes=True, backref="user")
        reviews = relationship("Review", passive_deletes=True, backref="user")
        amenity_ids = []
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
