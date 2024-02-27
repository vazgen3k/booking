from app.database import Base
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key= True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(nullable= False)
    description: Mapped[str] = mapped_column(nullable= True)
    price: Mapped[int] 
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int] 
    image_id: Mapped[int]

    hotels = relationship("Hotels", back_populates='rooms')

    def __str__(self):
        return self.name