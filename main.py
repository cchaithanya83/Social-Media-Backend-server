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
    """
    Create a new user.

    Parameters:
    - **user**: User information including email, hashed_password, and name.

    Returns:
    - **Success**: Returns a token for the created user.
    - **Error 400**: Email already in use.
    """
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
    """
    Generate an access token using OAuth2PasswordRequestForm.

    Parameters:
    - **form_data**: OAuth2 password request form containing username and password.

    Returns:
    - **Success**: Returns an access token.
    - **Error 401**: Invalid credentials.
    """
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
 
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
 
    return await _services.create_token(user)


@app.get("/api/users/myprofile", response_model=_common.User, tags=["users"])
async def get_user(user: _common.User = _fastapi.Depends(_services.get_current_user)):
    """
    Retrieve the current user's profile.

    Parameters:
    - **Authorization**: Bearer Token in the header.

    Returns:
    - **200 OK**: Successfully retrieved user profile.
    - **401 Unauthorized**: Not authenticated.
    """
    return user




@app.post("/api/createpost/")
async def create_post_route(
    post: _common.Post, 
    current_user: _common.User = _fastapi.Depends(_services.get_current_user)
):
    """
    Create a new post.

    Parameters:
    - **post**: Post information including content.
    - **current_user**: The user creating the post.

    Returns:
    - Success message.
    """
    db = next(_services.get_db())
    return await _services.create_post(email=current_user.email, post=post, db=db)



@app.get("/api/posts/", response_model=List[_common.Post])
async def list_posts(offset: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    List posts.

    Parameters:
    - **offset**: Offset for pagination.
    - **limit**: Limit for pagination.

    Returns:
    - List of posts.
    """
    return await _services.get_all_posts(db=db, offset=offset, limit=limit)


@app.post("/api/users/follow/{username}")
async def follow_user_route(username: str, current_user: _common.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Follow a user.

    Parameters:
    - **username**: Username to follow.
    - **current_user**: The user who is performing the follow action.

    Returns:
    - Success message.
    """
    return await _services.follow_user(followed_email=username, current_user=current_user, db=db)

@app.post("/api/users/unfollow/{username}")
async def unfollow_user_route(username: str, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Unfollow a user.

    Parameters:
    - **username**: Username to unfollow.
    - **current_user**: The user who is performing the unfollow action.

    Returns:
    - Success message.
    """
    return await _services.unfollow_user(followed_email=username, current_user=current_user, db=db)

@app.get("/api/users/followers", response_model=List[_common.Users])
async def get_followers_route(current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Get followers of the current user.

    Parameters:
    - **current_user**: The user whose followers are being retrieved.

    Returns:
    - List of followers.
    """
    return await _services.get_followers(email=current_user.email, db=db)


@app.delete("/api/dpost/{post_id}")
async def delete_post_route(post_id: int, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Delete a post.

    Parameters:
    - **post_id**: ID of the post to delete.
    - **current_user**: The user who is deleting the post.

    Returns:
    - Success message.
    """
    return await _services.delete_post(post_id=post_id, current_user=current_user, db=db)

@app.put("/api/upost/{post_id}")
async def update_post_route(post_id: int, new_content: str, current_user: _common.Users = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Update a post.

    Parameters:
    - **post_id**: ID of the post to update.
    - **new_content**: New content for the post.
    - **current_user**: The user who is updating the post.

    Returns:
    - Success message.
    """
    return await _services.update_post(post_id=post_id, new_content=new_content, current_user=current_user, db=db)


@app.delete("/api/users/delete")
async def delete_user_route(
    password: str,
    email: str,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    """
    Delete a user.

    Parameters:
    - **password**: User's password for authentication.
    - **email**: Email of the user to delete.

    Returns:
    - Success message.
    """
    return await _services.delete_user_with_password(
        email=email, password=password, db=db
    )


@app.post("/api/login")
async def login_route(response: _fastapi.Response, form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Generate an access token using OAuth2PasswordRequestForm.

    Parameters:
    - **form_data**: OAuth2 password request form containing username and password.

    Returns:
    - **Success**: Returns an access token.
    - **Error 401**: Invalid credentials.
    """
    return await _services.login_user(form_data=form_data, db=db)

@app.get("/api/users/", response_model=List[_common.User])
async def get_all_users(offset: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Get a list of all users.

    Parameters:
    - **offset** (optional): Offset for pagination.
    - **limit** (optional): Limit for pagination.

    Returns:
    - List of users.
    """
    return await _services.list_users(db=db, offset=offset, limit=limit)




