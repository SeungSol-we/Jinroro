from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Alembic이 모든 모델을 인식하려면 여기서 import 해야 함
from app.modules.auth.models import *       # noqa
from app.modules.users.models import *      # noqa
from app.modules.balance.models import *    # noqa
from app.modules.company.models import *    # noqa
from app.modules.fun.models import *        # noqa
