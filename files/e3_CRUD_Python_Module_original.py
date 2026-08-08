# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'howler1' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d/?authSource=%s' % (USER,PASS,HOST,PORT, DB)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            try:
                result = self.database.animals.insert_one(data)  # data should be dictionary
                if result.inserted_id:
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Error during insert: {e}")
                return False
        else: 
            print("Nothing to save, because data parameter is empty.")
            return False

    # Create method to implement the R in CRUD.
    def read(self, query):
        try:
            if query is not None:
                cursor = self.database.animals.find(query)
                result = list(cursor)
                return result
            else:
                return []
        except Exception as e:
            print(f"Error during query: {e}")
            return []

    def update(self, query, update_data):
        try:
            if query is not None and update_data is not None:
                result = self.database.animals.update_many(query, {"$set": update_data})
                return result.modified_count
            else:
                print("Query and update data cannot be empty")
                return 0
        except Exception as e:
            print(f"Error during update: {e}")
            return 0
    
    
    def delete(self, query):
        try:
            if query is not None:
                result = self.database.animals.delete_many(query)
                return result.deleted_count
            else:
                print("Query cannot be empty")
                return 0
        except Exception as e:
            print(f"Error during delete: {e}")
            return 0
        