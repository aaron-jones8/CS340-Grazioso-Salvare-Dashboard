from pymongo import MongoClient 
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(
        self,
        username: str = "aacuser",
        password: str = "password123",
        host: str = "localhost",
        port: int = 27017,
        auth_db: str = "admin",
        db_name: str = "aac",
        collection_name: str = "animals"
    ):
        """
        Initialize the MongoClient and set database/collection handles.
        
        By default this connects as user 'aacuser' with password 'password123'
        to the 'aac' database and 'animals' collection.
        """
        try:
            # Build MongoDB URI and authenticate against the admin databasee
            uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_db}"
            self.client = MongoClient(uri)
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]
        except PyMongoError as e:
            print(f"ERROR: Could not connect to MongoDB: {e}")
            self.client = None
            self.database = None
            self.collection = None
            
    # ---------- C: CREATE ---------- 
    
    def create(self, data: dict) -> bool:
        """
        Insert a single document into the collection.
        
        """
        if self.collection is None:
            return False
        
        if not isinstance(data, dict) or not data:
            # Data must be a non-empty dictionary
            return False
        
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError as e:
            print(f"ERROR in create(): {e}")
            return False

    # ---------- R: READ ----------
    def read(self, query: dict) -> list:
        """
        Query for documents in the collection.
        
        """
        if self.collection is None:
            return []
        
        if query is None:
            query = {}
            
        if not isinstance(query, dict):
            return []
        
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError as e:
            print(f"ERROR in read(): {e}")
            return []
    