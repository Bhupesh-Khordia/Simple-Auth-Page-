import gradio as gr
import requests

# API settings
API_URL = "https://simple-auth-page-backend.onrender.com"

# JWT token storage (in real app, use secure session storage)
current_session = {"token": None, "username": None, "role": None}

def get_auth_headers():
    """Get authorization headers with JWT token"""
    if current_session["token"]:
        return {"Authorization": f"Bearer {current_session['token']}"}
    return {}


def login_user(username, password):
    """Login user with OAuth2 form data and get JWT token"""
    try:
        # Use form data for OAuth2PasswordRequestForm
        response = requests.post(f"{API_URL}/login", data={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            
            # Store token and get user info
            current_session["token"] = token
            current_session["username"] = username
            
            # Get user profile to determine role
            profile_response = requests.get(f"{API_URL}/profile", headers=get_auth_headers())
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                current_session["role"] = profile_data["role"]
                return f"✅ Login successful! Welcome {profile_data['full_name']} ({profile_data['role']})"
            else:
                return "✅ Login successful but couldn't fetch profile"
        else:
            error_detail = response.json().get("detail", "Unknown error")
            return f"❌ Login failed: {error_detail}"
            
    except Exception as e:
        return f"❌ Error: {e}"


def get_user_profile():
    """Get current user's profile using JWT token"""
    if not current_session["token"]:
        return "❌ Please login first"
    
    try:
        response = requests.get(f"{API_URL}/profile", headers=get_auth_headers())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            current_session.clear()  # Clear invalid session
            return "❌ Session expired, please login again"
        else:
            return f"❌ Error getting profile: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"


def get_all_users():
    """Get list of all users (admin only) using JWT token"""
    if not current_session["token"]:
        return "❌ Please login first"
    
    if current_session["role"] != "admin":
        return "❌ Admin access required"
    
    try:
        response = requests.get(f"{API_URL}/users", headers=get_auth_headers())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            current_session.clear()
            return "❌ Session expired, please login again"
        elif response.status_code == 403:
            return "❌ Access forbidden - admin role required"
        else:
            return f"❌ Error getting users: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

def create_new_user(username, full_name, password, role):
    """Create a new user (admin only) using JWT token"""
    if not current_session["token"]:
        return "❌ Please login first"
    
    if current_session["role"] != "admin":
        return "❌ Admin access required"
    
    if not username or not full_name or not password:
        return "❌ Please fill all fields"
    
    try:
        response = requests.post(f"{API_URL}/create_user", 
            params={
                "username": username,
                "full_name": full_name,
                "password": password,
                "role": role
            },
            headers=get_auth_headers()
        )
        
        if response.status_code == 200:
            return f"✅ User {username} created successfully with {role} role!"
        elif response.status_code == 400:
            return "❌ User already exists"
        elif response.status_code == 401:
            current_session.clear()
            return "❌ Session expired, please login again"
        elif response.status_code == 403:
            return "❌ Access forbidden - admin role required"
        else:
            return f"❌ Error creating user: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"


def logout_user():
    """Logout user by clearing session"""
    current_session.clear()
    return "✅ Logged out successfully"

def create_simple_ui():
    """Create Gradio interface with JWT authentication"""
    with gr.Blocks(title="JWT Auth Demo") as app:
        gr.Markdown("# 🔐 JWT Authentication Demo")
        gr.Markdown("**Features:** Bcrypt password hashing + JWT tokens + OAuth2")
        
        # Login Section
        gr.Markdown("## 🔑 Login")
        with gr.Row():
            username_input = gr.Textbox(label="Username", placeholder="admin or user001")
            password_input = gr.Textbox(label="Password", type="password", placeholder="admin123 or pass001")
        with gr.Row():
            login_button = gr.Button("Login", variant="primary")
            logout_button = gr.Button("Logout", variant="secondary")
        login_result = gr.Textbox(label="Login Status", interactive=False)
        
        # Profile Section
        gr.Markdown("## 👤 My Profile")
        profile_button = gr.Button("Get My Profile (Requires JWT Token)")
        profile_result = gr.JSON(label="Profile Data")
        
        # Admin Section
        gr.Markdown("## 👑 Admin Panel")
        users_button = gr.Button("List All Users (Admin + JWT Required)")
        users_result = gr.JSON(label="All Users")
        
        gr.Markdown("### Create New User (Admin Only)")
        with gr.Row():
            new_username = gr.Textbox(label="Username")
            new_fullname = gr.Textbox(label="Full Name")
        with gr.Row():
            new_password = gr.Textbox(label="Password", type="password")
            new_role = gr.Dropdown(["user", "admin"], label="Role", value="user")
        create_button = gr.Button("Create User (Admin + JWT Required)")
        create_result = gr.Textbox(label="Creation Result", interactive=False)
        
        # Connect buttons to functions
        login_button.click(login_user, inputs=[username_input, password_input], outputs=login_result)
        logout_button.click(logout_user, outputs=login_result)
        profile_button.click(get_user_profile, outputs=profile_result)
        users_button.click(get_all_users, outputs=users_result)
        create_button.click(create_new_user, inputs=[new_username, new_fullname, new_password, new_role], outputs=create_result)
    
    return app


if __name__ == "__main__":
    print("🚀 Starting JWT-authenticated Gradio app...")
    print("🔗 Make sure backend is running at http://127.0.0.1:8000")
    print("📚 Swagger docs available at: http://127.0.0.1:8000/docs")
    
    app = create_simple_ui()
    app.launch()