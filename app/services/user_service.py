import httpx
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging import outboundLogging
from app.core.security import create_register_token, hash_password
from app.core.vault import get_url_groq_service
from app.models.user import RegisteredUser, TwoFA, User
from app.schemas.user import UserCreate, UserRegister
from app.services.two_fa_service import two_fa_generate_code
from app.services.email_services import send_email_verification

def create_user_service(db: Session, user: UserCreate):
    userExists = db.query(User).filter(User.email == user.email).first()
    if userExists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hashed_password  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def register(db: Session, user: UserRegister):
    try:
        user_exists = db.query(User).filter(User.email == user.email).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="Email already registered")

        ttl = timedelta(minutes=15)
        now = datetime.utcnow()

        pending_latest = (
            db.query(RegisteredUser)
            .filter(
                RegisteredUser.email == user.email,
                RegisteredUser.is_verified == False,
            )
            .order_by(RegisteredUser.created_at.desc())
            .first()
        )

        if pending_latest:
            age = now - pending_latest.created_at

            if age < ttl:
                raise HTTPException(
                    status_code=400,
                    detail="A registration attempt was made recently. Please check your email for the verification code or try again later.",
                )

            pendings = (
                db.query(RegisteredUser)
                .filter(
                    RegisteredUser.email == user.email,
                    RegisteredUser.is_verified == False,
                )
                .all()
            )

            for p in pendings:
                db.query(TwoFA).filter(TwoFA.user_id == p.id).delete(synchronize_session=False)
                db.delete(p)

            db.commit()

        hashed_password = hash_password(user.password)

        db_user_register = RegisteredUser(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password=hashed_password,
        )

        code = two_fa_generate_code(db)

        two_fa_entry = TwoFA(
            code=code,
            enabled=False,
            user=db_user_register,
        )

        db.add(db_user_register)
        db.add(two_fa_entry)
        db.commit()

        await send_email_verification(
            to=user.email,
            subject="Email Verification Code",
            code=code,
        )

        return code

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error processing registration.")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error during registration")

async def confirm_registration(db: Session, code: str):
    try:
        ttl = timedelta(minutes=15)
        now = datetime.utcnow()

        two_fa_entry = db.query(TwoFA).filter(TwoFA.code == code).first()
        if not two_fa_entry:
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        registered_user = two_fa_entry.user
        if not registered_user or registered_user.is_verified:
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        created_at = getattr(two_fa_entry, "created_at", None) or getattr(registered_user, "created_at", None)
        if not created_at or (now - created_at) > ttl:
            raise HTTPException(status_code=400, detail="Verification code has expired.")

        if db.query(User).filter(User.email == registered_user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered.")

        register_token = create_register_token(
            user_id=registered_user.id,
            email=registered_user.email,
            password=registered_user.password,
            first_name=registered_user.firstname,
            last_name=registered_user.lastname
        )

        external_service_url = f"{get_url_groq_service()}/users/register/external"
        
        payload = {
            "firstname": registered_user.firstname,
            "lastname": registered_user.lastname,
            "email": registered_user.email,
            "password": registered_user.password,
        }

        headers = {
            "Authorization": f"Bearer {register_token}",
            "Content-Type": "application/json",
        }

        try:
            async with outboundLogging(db, operation="Register user in external service") as client:
                resp = await client.post(external_service_url, json=payload, headers=headers)

            resp.raise_for_status()

        except httpx.HTTPStatusError as http_err:
            raise HTTPException(status_code=502, detail=f"External service error: {http_err.response.status_code}")
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Error communicating with external service.")

        body = {}
        if resp.headers.get("content-type", "").startswith("application/json"):
            body = resp.json()

        if body.get("status") != "success":
            raise HTTPException(status_code=500, detail="Error registering user in external service.")

        db_user = User(
            firstname=registered_user.firstname,
            lastname=registered_user.lastname,
            email=registered_user.email,
            password=registered_user.password,
            api_key=body.get("api_key")
        )
        db.add(db_user)

        registered_user.is_verified = True
        db.delete(two_fa_entry)

        db.commit()
        return registered_user

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error confirming registration.")
    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error during registration confirmation")

def get_users_service(db: Session):
    return db.query(User).all()

def get_user_service_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

def get_user_service_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()