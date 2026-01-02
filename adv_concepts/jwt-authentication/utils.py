from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

# Initialize fake_user_db lazily to avoid hashing at import time
fake_user_db = None

def _init_user_db():
    global fake_user_db
    if fake_user_db is None:
        fake_user_db = {
            'johndoe': {
                'username': 'johndoe',
                'hashed_password': pwd_context.hash('secret123')
            }
        }
    return fake_user_db

def get_user(username: str):
    db = _init_user_db()
    user = db.get(username)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)