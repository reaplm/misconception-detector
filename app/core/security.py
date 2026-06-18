from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import bcrypt

# Secret key to sign JWT tokens (Keep this private!)
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # 1. Convert the plain text string into bytes (UTF-8 encoding)
    password_bytes = password.encode('utf-8')
    
    # 2. Generate a random secure salt string
    salt = bcrypt.gensalt()
    
    # 3. Hash the password bytes and decode back into a clean string to save to Postgres
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 1. Convert the plain text password from login into bytes
    plain_bytes = plain_password.encode('utf-8')
    
    # 2. Convert the scrambled database string back into bytes
    hashed_bytes = hashed_password.encode('utf-8')
    
    # 3. Use bcrypt's built-in secure comparison function (Returns True or False)
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
