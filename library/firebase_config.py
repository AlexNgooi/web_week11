import firebase_admin
from firebase_admin import credentials, db as firebase_db
import os
from pathlib import Path

# Initialize Firebase app as a module-level variable
firebase_app = None
db = None

def initialize_firebase():
    """Initialize Firebase if not already initialized"""
    global firebase_app, db
    
    try:
        # Check if already initialized
        if firebase_app is not None:
            return firebase_app
            
        # Check if Firebase is already initialized by checking _apps
        if firebase_admin._apps:
            firebase_app = firebase_admin.get_app()
            db = firebase_db
            return firebase_app
        
        # Get the base directory
        BASE_DIR = Path(__file__).resolve().parent.parent
        
        # Path to Firebase credentials
        cred_path = os.path.join(BASE_DIR, "firebase_key.json")
        
        # Check if credentials file exists
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase credentials file not found at: {cred_path}")
        
        # Initialize Firebase
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://web-libraryproject-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        
        # Set the db reference
        db = firebase_db
        
        print("Firebase initialized successfully!")
        return firebase_app
        
    except Exception as e:
        print(f"ERROR initializing Firebase: {e}")
        import traceback
        traceback.print_exc()
        raise

# Initialize Firebase when module is imported
initialize_firebase()