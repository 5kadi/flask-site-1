import database_mod
import sqlite3 as sq

class UserLogin():
    def get_user(self, id):
        self.__user = id
        print(self.__user)
        return self

    def create_user(self, id):
        self.__user = id
        print(self.__user, "created")
        return self
    
    def get_admin_user(self, id, permission):
        self.__user = id
        self.__perm = permission
        return self

    def create_admin_user(self, id, permission):
        self.__user = id
        self.__perm = permission
        return self

    def is_authenticated():
        return True
    
    def is_active():
        return True
    
    def is_anonymous():
        return False
    
    def get_id(self):
        return str(self.__user)

