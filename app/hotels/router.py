from fastapi import APIRouter, Depends, Query
from app.hotels.dao import HotelDAO
from app.bookings.schemas import SBooking
from app.Users.dependencies import get_current_user
from app.Users.models import Users
from datetime import date, datetime, timedelta
from app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod
from typing import Optional, List
from app.hotels.shemas import SHotel, SHotelInfo
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}/")
@cache(expire=60)
async def get_hotels(location: str, 
                     date_from: date = Query(..., description= f"Например, {datetime.now().date()}"), 
                     date_to: date = Query(..., description= f"Например, {(datetime.now() + timedelta(days=14)).date()}"), 
                     ) ->List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod 
    result = await HotelDAO.get_hotels(location, date_from, date_to)
    return result


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    result = await HotelDAO.find_by_id(hotel_id)
    return result
