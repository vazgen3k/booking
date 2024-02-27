import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", *[
    [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
    ])
async def test_add_and_get_booking( room_id, date_from, date_to, booked_rooms, 
                                   status_code, autontificated_ac: AsyncClient): 
    responce = await autontificated_ac.post("/booking", params= {
        "room_id": room_id, 
        "date_from": date_from, 
        "date_to": date_to
    } )
    assert responce.status_code == status_code

    responce = await autontificated_ac.get("/booking/all_bookings")

    assert len(responce.json()) == booked_rooms 


async def test_get_delete_bookings(autontificated_ac: AsyncClient):
    result = await autontificated_ac.get("/booking/all_bookings")
    existing_bookings = [booking["id"] for booking in result.json()]
    for booking_id in existing_bookings:
         await autontificated_ac.delete(f"/booking/{booking_id}")

    responce = await autontificated_ac.get("/booking/all_bookings")
    assert len(responce.json()) == 0

