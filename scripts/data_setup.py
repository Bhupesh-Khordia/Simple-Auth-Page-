"""
Script to create 100 users with bcrypt hashed passwords
Uses proper password hashing for security
"""
from pathlib import Path
import json
import random
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def generate_100_users():
    """Generate 100 users with hashed passwords"""
    users = {}
    
    # First create admin user with hashed password
    users["admin"] = {
        "username": "admin",
        "full_name": "Admin User", 
        "password": hash_password("admin123"),
        "role": "admin"
    }
    
    # List of common first and last names
    first_names = [
        "Alice", "Bob", "Charlie", "Diana", "Emma", "Frank", "Grace", "Henry",
        "Ivy", "Jack", "Kate", "Leo", "Mary", "Nick", "Olivia", "Paul",
        "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander",
        "Yara", "Zoe", "Alex", "Ben", "Chloe", "David", "Eva", "Felix"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark"
    ]
    
    # Generate 99 regular users (plus 1 admin = 100 total)
    for i in range(1, 100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        username = f"user{i:03d}"  # user001, user002, etc.
        full_name = f"{first_name} {last_name}"
        password = f"pass{i:03d}"  # pass001, pass002, etc.
        
        users[username] = {
            "username": username,
            "full_name": full_name,
            "password": hash_password(password),  # Hash the password
            "role": "user"
        }
    
    return users

def save_users_to_file():
    """Save users to JSON file"""
    # Save to parent directory (project root)
    data_file = Path(__file__).parent.parent / "users.json"
    
    print("Generating 100 users...")
    users = generate_100_users()
    
    with open(data_file, "w") as f:
        json.dump(users, f, indent=2)
    
    print(f"✅ Created {len(users)} users with bcrypt hashed passwords!")
    print(f"📁 Saved to: {data_file}")
    print("\n🔑 Login credentials (passwords are hashed in database):")
    print("👑 Admin: admin / admin123")
    print("👤 Users: user001 / pass001, user002 / pass002, etc.")
    print("📊 Total users: 1 admin + 99 regular users = 100 users")
    print("🔒 All passwords are securely hashed with bcrypt!")

if __name__ == "__main__":
    save_users_to_file()
