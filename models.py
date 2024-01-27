import datetime as _dt
 
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
 
import database as _database
 
class User(_database.Base):
    __tablename__ = "user"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    name = _sql.Column(_sql.String)
 
    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class post(_database.Base):
    __tablename__ = "post"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    post = _sql.Column(_sql.String)


class Follow(_database.Base):
    __tablename__ = "follow"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    follower_email = _sql.Column(_sql.String, index=True)
    followed_email = _sql.Column(_sql.String, index=True)   