from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

app = FastAPI()

# JWT Configuration
SECRET_KEY = "your_secret_key_here_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# File-based "database"
DATA_FILE = Path(__file__).parent.parent / "users.json"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def load_users():
    """Load users from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user = Depends(get_current_user)):
    """Require admin role"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Load users when server starts
users_db = load_users()


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with OAuth2 and return JWT token"""
    user = users_db.get(form_data.username)
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    """Get current user's profile"""
    return {
        "username": current_user["username"],
        "full_name": current_user["full_name"], 
        "role": current_user["role"]
    }


@app.get("/users")
def list_all_users(admin_user = Depends(require_admin)):
    """Get list of all users (admin only)"""
    users_list = []
    for user in users_db.values():
        users_list.append({
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"]
        })
    return {"users": users_list}

@app.post("/create_user")
def create_new_user(username: str, full_name: str, password: str, role: str, admin_user = Depends(require_admin)):
    """Create a new user (admin only)"""
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password before storing
    hashed_password = hash_password(password)
    
    users_db[username] = {
        "username": username,
        "full_name": full_name,
        "password": hashed_password,
        "role": role
    }
    save_users(users_db)
    return {"message": f"User {username} created successfully"}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server with JWT authentication...")
    print("API will be available at: http://127.0.0.1:8000")
    print("Swagger docs at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)