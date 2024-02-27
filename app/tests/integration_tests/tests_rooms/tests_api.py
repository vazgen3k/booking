from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('location,date_from,date_to,status_code', [
    ("Алтай", '2024-04-15', '2024-04-01', 400),
    ("Алтай", '2024-04-15', '2025-04-01', 400),
    ("Алтай", '2024-04-15', '2024-04-25', 200),
])
async def test_get_hotels(location, date_from, date_to, status_code, autontificated_ac: AsyncClient):
    responce =  await autontificated_ac.get(f"/hotels/{location}/", params={
        "location": location, 
        "date_from": date_from, 
        "date_to": date_to
    })

    assert responce.status_code == status_code

