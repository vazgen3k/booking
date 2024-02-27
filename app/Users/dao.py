from app.dao.base import BaseDAO
from app.Users.models import Users


class UserDAO(BaseDAO):
    model = Users