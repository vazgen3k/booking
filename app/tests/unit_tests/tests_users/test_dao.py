from app.Users.dao import UserDAO
import pytest

@pytest.mark.parametrize("user_id,email,is_exist", [
    (1, "test@test.com", True),
    (2, "artem@example.com", True), 
    (3, "email", False)
])
async def test_find_user_by_id(user_id, email, is_exist):
    user = await UserDAO.find_by_id(user_id)

    if is_exist:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user

