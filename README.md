# Social-Media-Backend-server

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the FastAPI Application
```bash
uvicorn main:app --reload
```

### 3. Visit http://127.0.0.1:8000/docs in your browser to access the Swagger UI for API documentation.


Usage:

1) /api/users - create User
2) /users/follow/{username} - Follow user
3) /api/createpost/ - create a new post
4) /api/posts/ - List all the post
5) /api/users/unfollow/{username} - unfollow th userr
6) /api/users/followers - list people who follow us
7) /api/dpost/{post_id} - delete the post by its id
8) /api/upost/{post_id} - update the post by its id
9) /api/users/delete - delte the user using email and password
10) /api/login - login 
11) /api/users/ - list all user
12) /api/users/myprofile - gives user details
13) /api/token - generates token







