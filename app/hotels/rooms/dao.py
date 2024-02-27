from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from datetime import date
from sqlalchemy import select, and_, or_, func, insert
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker, engine


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms(cls, hotel_id, date_from, date_to):
        booked_rooms =( 
            select(Bookings.room_id, (func.count(Bookings.room_id)).label('rooms_booked')).select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from>=date_from,  
                        Bookings.date_from <= date_to
                        ),
                    and_(
                        Bookings.date_from <= date_from,  
                        Bookings.date_to > date_from
                    ),
                )).group_by(Bookings.room_id)
                 .cte('booked_rooms'))
            
        free_rooms = (select(Rooms.__table__.columns, (Rooms.price*(date_to-date_from).days).label('total_cost'), func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left')).select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                     .where(Rooms.hotel_id == hotel_id).group_by(Rooms.id))
        async with async_session_maker() as session: 
            result = await session.execute(free_rooms)
            return result.mappings().all()
