# Social-Media-Backend-server


Disc:

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



Postman prerequisite: 

1) Createuser

post:   /api/users
body:  {
    "email": "21d12.chaithanya@sjec.ac.in",
    "hashed_password": "12345678"
}
header: Content-Type:application/json


2) create token
post:  /api/token
x-www-form-urlencoded:username:21d12.chaithanya@sjec.ac.in
                      password:12345678
header: Content-Type:application/x-www-form-urlencoded



