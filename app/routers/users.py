from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.schemes.message import Message
from app.services.user import schemes
from app.services.user.logic import UserLogic
from app.services.user.models import Users
from app.core import auth
from app.db.sessions import get_db
from app.core.exceptions.user import PasswordOrLoginDoesNotMatch, UserDoesNotExists, UserWithSameLoginExists
from pydantic import parse_obj_as

router = APIRouter()
logic = UserLogic(model=Users)
auth_handler = auth.AuthHandler()


@router.get("/user/refresh_token", tags=["user"], response_model=schemes.UserToken)
async def refresh_token(request: Request, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):
    return {"token": auth_handler.encode_token(user_id=request.user.id)}


@router.post(
    "/user",
    tags=["user"],
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": Message},
    },
    response_model_exclude={"id"},
)
async def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)):
    operation,res  = await logic.create_user(db=db, user=user, password=user.password)
    if not operation:
        raise HTTPException(detail=res.message, status_code=res.error_code)
    return res.__dict__


@router.post(
    "/user/login",
    tags=["user"],
    responses={401: {"model": Message}},
    status_code=status.HTTP_200_OK,
    response_model=schemes.UserToken
)
async def login(user: schemes.UserLogin, db: Session = Depends(get_db)):
    user_old = await logic.get_user_by_login(db, user.username)
    if user_old and await auth_handler.verify_password(
            plain_password=user.password, hash_password=user_old.password
    ):
        token = await auth_handler.encode_token(user_old.id)
        return {"token": token}
    raise HTTPException(
        status_code=PasswordOrLoginDoesNotMatch.error_code,
        detail=PasswordOrLoginDoesNotMatch.message,
    )


@router.get(
    "/users",
    response_model=List[schemes.User],
    tags=["user"],
    status_code=status.HTTP_200_OK
)
async def get_all_users(db: Session = Depends(get_db)):
    res = await logic.get_all(db)
    if not res:
        raise HTTPException(
            status_code=UserDoesNotExists.error_code,
            detail=UserDoesNotExists.message
        )
    return res

@router.get(
    "/user/{id}", response_model=schemes.User, tags=["user"], status_code=status.HTTP_200_OK
)
async def get_user_by_id(
        id: int,
        db: Session = Depends(get_db),
):
    res = await logic.get_user_by_id(db, id)

    print(res,'user')
    if not res:
        raise HTTPException(status_code=UserDoesNotExists.error_code, detail=UserDoesNotExists.message)
    return res


@router.get(
    "/user", response_model=schemes.User, tags=["user"], status_code=status.HTTP_200_OK
)
async def get_myself(
        request: Request,
        user=Depends(auth_handler.auth_wrapper),
        db: Session = Depends(get_db),
):
    res = await logic.get_user_by_id(db, user_id=request.user.id)
    return res


@router.patch(
    "/user/{username}",
    tags=["user"],
    responses={404: {"model": Message}},
    status_code=status.HTTP_200_OK,
)
async def patch_user(
        username: str, user: schemes.UserPatch, db: Session = Depends(get_db)
):
    res = await logic.get_user_by_login(db, user.username)
    if res:
        raise HTTPException(status_code=UserWithSameLoginExists.error_code, detail=UserWithSameLoginExists.message)

    operation, res = await logic.patch_user(db=db, user=user, username=username)

    if not operation:
        raise HTTPException(detail=res.message, status_code=res.error_code)
    return res
