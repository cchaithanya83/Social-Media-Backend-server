import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database
import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy as _sql
import common as _common , models as _models , services as _services

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "chaithanya"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60
async def create_user(user: _common.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password), name=user.name
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

    
def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)
 
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user
 
 
async def create_token(user: _models.User):
    user_obj = _common.User.from_orm(user)

    expiration_time = _dt.datetime.utcnow() + _dt.timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    token_data = {
        "sub": str(user_obj.id),
        "exp": expiration_time,
    }

    token = _jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token, "token_type": "bearer", "expires_in": JWT_EXPIRATION_TIME_MINUTES * 60}

 
async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        print(payload)
        user = db.query(_models.User).get(payload["sub"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
 
    return _common.User.from_orm(user)





async def create_post(email: str, post: _common.Post, db: _orm.Session):
    new_post = _models.post(email=email, post=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


async def get_all_posts(db: _orm.Session, offset: int = 0, limit: int = 10):
    posts = db.query(_models.post).order_by(_models.post.id).offset(offset).limit(limit).all()
    
    print("Debug: Number of posts retrieved:", len(posts))  # used for testing only remove it 
    
    return [_common.Post(email=post.email, content=post.post) for post in posts]

#chatgpt fastapi2


async def follow_user(followed_email: str, current_user: _common.Users, db: _orm.Session):
    follow_instance = _models.Follow(follower_email=current_user.email, followed_email=followed_email)
    db.add(follow_instance)
    db.commit()
    db.refresh(follow_instance)
    return {"message": "User followed successfully"}

async def unfollow_user(followed_email: str, current_user: _common.Users, db: _orm.Session):
    follow_instance = db.query(_models.Follow).filter(
        _models.Follow.follower_email == current_user.email,
        _models.Follow.followed_email == followed_email
    ).first()

    if follow_instance:
        db.delete(follow_instance)
        db.commit()
        return {"message": "User unfollowed successfully"}  #tset
    else:
        return {"message": "User was not followed"}  #test

async def get_followers(email: str, db: _orm.Session):
    followers = db.query(_models.Follow).filter(_models.Follow.followed_email == email).all()
    return [_common.Users(email=follower.follower_email) for follower in followers]


async def delete_post(post_id: int, current_user: _common.Users, db: _orm.Session):
    post = db.query(_models.post).filter(
        _models.post.id == post_id,
        _models.post.email == current_user.email
    ).first()

    if post:
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Post not found")

async def update_post(post_id: int, new_content: str, current_user: _common.Users, db: _orm.Session):
    post = db.query(_models.post).filter(
        _models.post.id == post_id,
        _models.post.email == current_user.email
    ).first()

    if post:
        post.post = new_content
        db.commit()
        db.refresh(post)
        return {"message": "Post updated successfully"}
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Post not found")


async def delete_user_with_password(
    email: str, password: str, db: _orm.Session
):
    user = await _services.authenticate_user(
        email=email, password=password, db=db
    )

    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Password or User not found"
        )
    
async def login_user(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
 
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
 
    return await _services.create_token(user)


async def list_users(db: _orm.Session, offset: int = 0, limit: int = 10):
    users = db.query(_models.User).offset(offset).limit(limit).all()
    return users