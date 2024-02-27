from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.Users.dependencies import get_current_user
from app.Users.models import Users
from datetime import date
from app.exceptions import RoomCannotBeBooked, BookCannotBeDelete
from app.tasks.tasks import send_booking_confirmation_email
from pydantic import parse_obj_as, TypeAdapter
from typing import List

router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"]
)

@router.get("/all_bookings")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id = user.id)


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add_book(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking
   
    
@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    result = await BookingDAO.delete_booking(user_id = user.id, booking_id = booking_id)
    if not result:
        raise BookCannotBeDelete
    return result

