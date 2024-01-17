#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ Place Class subclass of BaseModel """
    __tablename__ = "places"
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []

        reviews = relationship("Review", backref="place", passive_deletes=True)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        reviews = []

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Getter for reviews"""
            from models import storage
            from models.review import Review
            review_list = []
            for key, value in storage.all(Review).items():
                if value.place_id == self.id:
                    review_list.append(value)
            return review_list

        @property
        def amenities(self):
            """Getter for amenities"""
            from models import storage
            from models.amenity import Amenity
            amenity_list = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenity_list.append(value)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities"""
            from models.amenity import Amenity
            if obj and type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
