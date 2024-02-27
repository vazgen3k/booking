import pytest
from app.bookings.dao import BookingDAO
from datetime import datetime


@pytest.mark.parametrize('user_id,room_id,date_from,date_to', [
    (1, 2, '2024-05-05', '2024-05-25'),
    (1, 2, '2024-06-06', '2024-06-25')
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    new_booking = await BookingDAO.add_book(
        user_id = user_id, 
        room_id = room_id, 
        date_from = datetime.strptime(date_from, "%Y-%m-%d"), 
        date_to =  datetime.strptime(date_to, "%Y-%m-%d"), 
    )
    assert new_booking.user_id == 1
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    print(new_booking)
    assert new_booking is not None

    await BookingDAO.delete(user_id = user_id, id = new_booking.id)
    
    deleted_booking = await BookingDAO.find_one_or_none(id=5)
 
    assert deleted_booking is None
  