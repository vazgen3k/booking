from fastapi import Query
from app.hotels.rooms.dao import RoomsDAO
from datetime import date
from app.hotels.router import router
from datetime import date, datetime, timedelta
from app.hotels.rooms.shemas import SRoomInfo
from typing import List

@router.get("/{hotel_id}/rooms/")
async def get_rooms(hotel_id: int, 
            date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
            date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")) ->List[SRoomInfo]:
    
    result = await RoomsDAO.get_rooms(hotel_id, date_from, date_to)
    return result
