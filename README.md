# FastAPI + Gradio JWT Authentication Demo

**A professional authentication system with bcrypt password hashing and JWT tokens.**

## 🔐 Security Features
- ✅ **Bcrypt password hashing** - Secure password storage
- ✅ **JWT tokens** - Stateless authentication
- ✅ **OAuth2 flow** - Industry standard login
- ✅ **Role-based access** - Admin/User permissions
- ✅ **Token expiration** - 30-minute sessions

## Project Structure
```
auth_page/
├── backend/
│   └── main.py          # FastAPI with JWT + bcrypt
├── frontend/
│   └── app.py           # Gradio UI with token handling
├── scripts/
│   └── data_setup.py    # Creates 100 users with hashed passwords
├── requirements.txt     # JWT + bcrypt dependencies
├── users.json          # Encrypted user database
└── README.md           # This file
```

## Quick Start

### 1. Install Dependencies
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install JWT + bcrypt packages
pip install -r auth_page/requirements.txt
```

### 2. Generate Encrypted Users
```powershell
cd auth_page\scripts
python data_setup.py
```
This creates 100 users with bcrypt-hashed passwords!

### 3. Start Backend Server
```powershell
cd auth_page\backend
python main.py
```
- Backend runs at http://127.0.0.1:8000
- Swagger docs at http://127.0.0.1:8000/docs

### 4. Launch Frontend
```powershell
# New terminal
cd auth_page\frontend
python app.py
```
Gradio UI opens automatically with JWT authentication!

## 🔑 Test Credentials
- **Admin:** `admin` / `admin123`
- **Users:** `user001` / `pass001`, `user002` / `pass002`, etc.
- **Total:** 100 users (1 admin + 99 regular users)
- **Security:** All passwords are bcrypt-hashed in database

## 🛡️ How It Works

### Backend Security
1. **Password Hashing:** Uses bcrypt to hash passwords
2. **JWT Tokens:** Creates signed tokens with user info + expiration
3. **Token Validation:** Every protected endpoint verifies JWT
4. **Role Checking:** Admin endpoints require admin role in token

### Frontend Authentication
1. **OAuth2 Login:** Sends credentials via form data
2. **Token Storage:** Stores JWT in memory (session-based)
3. **Authenticated Requests:** Includes `Authorization: Bearer <token>` header
4. **Automatic Logout:** Clears session on token expiration

## API Endpoints

### Public
- `POST /login` - OAuth2 login (returns JWT token)

### Protected (Requires JWT)
- `GET /profile` - Get current user profile
- `GET /users` - List all users (admin only)
- `POST /create_user` - Create new user (admin only)
- `GET /admin` - Admin dashboard (admin only)

## 🚀 Advanced Features
- **Swagger UI:** Interactive API docs at `/docs`
- **Automatic token expiry:** 30-minute sessions
- **Error handling:** Proper HTTP status codes
- **Security headers:** Bearer token authentication
- **Input validation:** FastAPI request validation

Perfect for learning professional authentication patterns!