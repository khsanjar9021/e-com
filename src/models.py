from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Text, Float
from sqlalchemy.orm import relationship
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType, ImageType
from .db import Base


storage = FileSystemStorage(path="static/tmp")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float, index=True)
    lower_power = Column(Float, index=True)
    lower_current = Column(Float, index=True)
    lower_voltage = Column(Float, index=True)
    size = Column(String, index=True)
    country = Column(String, index=True)
    description = Column(Text, index=True)
    file = Column(ImageType(storage=storage))
    file_2 = Column(ImageType(storage=storage))
    file_3 = Column(ImageType(storage=storage))
    file_4 = Column(ImageType(storage=storage))
    file_5 = Column(ImageType(storage=storage))
    file_6 = Column(ImageType(storage=storage))
    file_7 = Column(ImageType(storage=storage))
    video = Column(FileType(storage=storage))


    type = relationship("Catalogue", back_populates="item")

    catalogue_id = Column(Integer, ForeignKey("catalogue.id"))




class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    text = Column(Text, index=True)


class Catalogue(Base):
    __tablename__ = "catalogue"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    item = relationship("Item", back_populates="type")

    def __str__(self):
        return self.name