# Social-Media-Backend-server


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



