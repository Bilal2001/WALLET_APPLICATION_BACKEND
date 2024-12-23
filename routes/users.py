from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from database import get_session
from models import CreateUser, User, UpdateUser
from uuid import uuid4

app = APIRouter(prefix="/users", tags=["users"])

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUser,
    session: Session = Depends(get_session)
) -> User:
    user = User(
        name=user_data.name, 
        email=user_data.email, 
        phone=user_data.phone
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_users(
    user_id: int,
    session: Session = Depends(get_session)
) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not Found")
    return user

@app.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_details_of_user(
    user_id: int,
    user_data: UpdateUser,
    session: Session = Depends(get_session)
) -> User:
    user_to_update = session.exec(select(User).where(User.id == user_id)).first()
    if user_to_update is None:
        raise HTTPException(status_code = 404, detail = "User not Found")

    if len(user_data.name): user_to_update.name = user_data.name
    if len(user_data.email): user_to_update.email = user_data.email
    if len(user_data.phone): user_to_update.phone = user_data.phone

    user_to_update.updated_at = datetime.now()
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return user_to_update


# #* Testing
@app.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    print(users)
    return users