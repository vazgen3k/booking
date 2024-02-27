from app.database import Base
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


""" class Users(Base):
    __tablename__ = 'users' """

"""     id = Column(Integer, primary_key = True)
    email = Column(String)
    hashed_password = Column(String, nullable=False)
 """

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    user_bookings = relationship("Bookings", back_populates="bookings_user")

    def __str__(self):
        return f'User {self.email}'