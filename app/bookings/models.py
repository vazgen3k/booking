from app.database import Base
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.orm import relationship


""" class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey('rooms.id'))
    user_id = Column(ForeignKey('users.id'))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
    total_days = Column(Integer, Computed('date_to - date_from')) """


class Bookings(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed('(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Computed('date_to - date_from'))

    bookings_user = relationship("Users", back_populates='user_bookings')

    def __str__(self):
        return f'Booking №{self.id}'