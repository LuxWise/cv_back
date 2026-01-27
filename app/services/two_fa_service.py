import random
from app.models.user import TwoFA
from sqlalchemy.orm import Session


def two_fa_generate_code(db: Session):
    code = str(random.randint(100000, 999999))
    code_exists = db.query(TwoFA).filter(TwoFA.code == code).first()

    if code_exists:
        return two_fa_generate_code(db)

    return code