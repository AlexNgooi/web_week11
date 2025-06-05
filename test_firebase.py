from library.firebase_config import db

try:
    ref = db.reference('test')
    ref.set({'test': 'Hello Firebase!'})
    print("Write successful!")
    
    data = ref.get()
    print(f"Read successful: {data}")
    
    ref.delete()
    print("Delete successful!")
except Exception as e:
    print(f"Error: {e}")