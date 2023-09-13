import pymysql
from flask_login.mixins import UserMixin
from extensions import bcrypt
import pymysql


class User(UserMixin):
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        super(User).__init__()

    def get_id(self):
        return self.username
    
    def check_password(self, input_password: str) -> str:
        return bcrypt.check_password_hash(self.password, input_password) 
    

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "Sairam12#"
        db = "summerREU"

        self.con = pymysql.connect(host=host, user=user, password=password, db = db, cursorclass = pymysql.cursors.DictCursor)
    
    def get_user_with_id(self, user_id: str) -> User:
        cursor = self.con.cursor()
        sql = "SELECT * FROM Users WHERE Users.UserName=%s"
        cursor.execute(sql, (user_id))
        user = cursor.fetchone()
        if user:
            user = User(user.get('UserName'), user.get('Password'))
        cursor.close()
        return user
    

if __name__ == "__main__":
    db = Database()
    user = db.get_user_with_id()
    print(user)