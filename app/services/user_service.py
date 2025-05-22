import bcrypt


class UserService:
    def __init__(self):
        pass

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())