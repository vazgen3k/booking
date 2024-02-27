from app.database import Base
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


""" class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key= True)
    name = Column(String, nullable= False)
    location = Column(String, nullable= False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable= False)
    image_id = Column(Integer) """

""" 
class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key= True)
    hotel_id = Column(ForeignKey('hotels.id'))
    name = Column(String, nullable= False)
    description = Column(String) 
    price = Column(Integer)
    services = Column(JSON)
    quantity = Column(Integer)
    image_id = Column(Integer) """


class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(nullable= False)
    location: Mapped[str] = mapped_column(nullable= False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable= False)
    image_id: Mapped[int]

    rooms = relationship("Rooms", back_populates='hotels')

    def __str__(self):
        return self.name

