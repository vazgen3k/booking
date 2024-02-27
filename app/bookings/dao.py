from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from datetime import date
from sqlalchemy import select, and_, or_, func
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker
from app.exceptions import IncorrectDate
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger



class BookingDAO(BaseDAO):
    model = Bookings
    @classmethod
    async def add_book(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        
        try:
            if date_from >= date_to or (date_to - date_from).days >= 30:
                raise IncorrectDate

            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(Bookings.room_id == room_id),
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # print(get_rooms_left.compile(engine, compile_kwargs = {'literal_binds': True} ))

                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price = price.scalar()
                    add_booking = await super().add(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    return add_booking.scalar()

                else:
                    return None
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg="Database Exc"

            elif isinstance(err, Exception):
                msg = "Unknown Exc"
            msg +=": Cannot be booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to
            }
            logger.error(msg, extra=extra,  exc_info=True)
            

    @classmethod
    async def delete_booking(cls, user_id, booking_id):
        find_one_or_none = await super().find_one_or_none(
                    user_id=user_id, id=booking_id
                )
   
        if not find_one_or_none:
            return None
        query = await BookingDAO.delete(user_id=user_id, id=booking_id)
        return query
