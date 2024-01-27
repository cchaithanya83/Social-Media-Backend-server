from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import datetime as _dt 
import pydantic as _pydantic
import sqlalchemy.orm as _orm
 
import services as _services, common as _common, models as _models
 
app = _fastapi.FastAPI()



@app.post("/api/users")
async def create_user(
    user: _common.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")
 
    user = await _services.create_user(user, db)
 
    return await _services.create_token(user)



@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
 
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
 
    return await _services.create_token(user)


@app.get("/api/users/myprofile", response_model=_common.User)
async def get_user(user: _common.User = _fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/users/follow/{username}")
def follow_user(username: str, current_user: _common.Users = _fastapi.Depends(_services.get_current_user)):
    
    pass


@app.post("/api/createpost/")
async def create_post_route(post: _common.Post, current_user: _common.Users = _fastapi.Depends(_services.get_current_user)):
    db = next(_services.get_db())
    return await _services.create_post(email=current_user.email, post=post, db=db)



@app.get("/api/posts/", response_model=List[_common.Post])
async def list_posts(offset: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_posts(db=db, offset=offset, limit=limit)


@app.post("/api/users/follow/{username}")
async def follow_user_route(username: str, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.follow_user(followed_email=username, current_user=current_user, db=db)

@app.post("/api/users/unfollow/{username}")
async def unfollow_user_route(username: str, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.unfollow_user(followed_email=username, current_user=current_user, db=db)

@app.get("/api/users/followers", response_model=List[_common.Users])
async def get_followers_route(current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_followers(email=current_user.email, db=db)


@app.delete("/api/post/{post_id}")
async def delete_post_route(post_id: int, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.delete_post(post_id=post_id, current_user=current_user, db=db)

@app.put("/api/post/{post_id}")
async def update_post_route(post_id: int, new_content: str, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.update_post(post_id=post_id, new_content=new_content, current_user=current_user, db=db)


@app.delete("/api/users/delete")
async def delete_user_route(
    password: str,
    email: str,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.delete_user_with_password(
        email=email, password=password, db=db
    )


@app.post("/api/login")
async def login_route(response: _fastapi.Response, form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.login_user(form_data=form_data, db=db)

@app.get("/api/users/", response_model=List[_common.User])
async def get_all_users(offset: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.list_users(db=db, offset=offset, limit=limit)
