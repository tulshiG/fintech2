from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.database import get_db_connection
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Auth"])

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Register new user
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.database import get_db_connection
from passlib.context import CryptContext
import mysql.connector

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define Pydantic model for request body
class RegisterRequest(BaseModel):
    pan_no: str
    username: str
    password: str

# Hash password function
def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/register")
def register(user: RegisterRequest):
    connection = get_db_connection()
    cursor = connection.cursor()
    password_hash = hash_password(user.password)

    print(f"🔍 DEBUG: Inserting -> PAN: {user.pan_no}, Username: {user.username}")  # Debug line

    try:
        cursor.execute("INSERT INTO users (pan_no, username, password_hash) VALUES (%s, %s, %s)", 
                       (user.pan_no, user.username, password_hash))
        connection.commit()
        print("✅ INSERT successful")  # Debugging message
    except mysql.connector.IntegrityError:
        print("❌ Duplicate PAN Number")
        raise HTTPException(status_code=400, detail="PAN number already exists")
    except Exception as e:
        print(f"🔥 ERROR: {e}")  # Debugging error
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()
        connection.close()

    return {"message": "User registered successfully"}

# Login and get token
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE pan_no = %s", (form_data.username,))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(data={"sub": user["pan_no"]})
    
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        pan_no: str = payload.get("sub")
        if pan_no is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"pan_no": pan_no}