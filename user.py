from flask_login import UserMixin
from passlib.hash import sha256_crypt
from model import *

class User(UserMixin):

    def __init__(self, email, password):
        self.db = model()
        self.query = self.db(self.db.user.email == email)

        if self.query.isempty() is False:
            self.userId = self.query.select(
                self.db.user.id, self.db.user.password, self.db.user.name).first()

            self.email = email
            self.name = self.userId.name
            self.password = password
    
    def is_authenticated(self):
      if(self.query.isempty() is True):
        return False
      if sha256_crypt.verify(self.password, self.userId.password):
        return True
      return False

    def is_active(self):
      return True

    def is_anonymous(self):
      return False
    
    def get_id(self):
      if(self.query.isempty() is True):
        return False

      return self.email

    @classmethod
    def get_user(cls, user_id):
      db = model()
      query = db(db.user.email == user_id)
      if query.isempty() is True:
        return None
      user = query.select(db.user.email, db.user.password).first()
      return cls(user.email, user.password)
