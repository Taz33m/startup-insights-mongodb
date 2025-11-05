"""
MongoDB Atlas connection and data insertion script.
This module handles database connections, collection setup, and data ingestion.
"""
import json
from typing import List, Dict, Any
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import config


class MongoDBHandler:
    """Handler for MongoDB Atlas operations."""
    
    def __init__(self, uri: str = None, db_name: str = None):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection string (defaults to config.MONGODB_URI)
            db_name: Database name (defaults to config.DATABASE_NAME)
        """
        self.uri = uri or config.MONGODB_URI
        self.db_name = db_name or config.DATABASE_NAME
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish connection to MongoDB Atlas."""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"✅ Successfully connected to MongoDB Atlas!")
            print(f"📊 Database: {self.db_name}")
            return True
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("🔒 MongoDB connection closed.")
    
    def create_collection(self, collection_name: str = None):
        """
        Create a collection with indexes.
        
        Args:
            collection_name: Name of the collection (defaults to config.COLLECTION_NAME)
        """
        collection_name = collection_name or config.COLLECTION_NAME
        
        if collection_name in self.db.list_collection_names():
            print(f"ℹ️  Collection '{collection_name}' already exists.")
            return self.db[collection_name]
        
        collection = self.db[collection_name]
        
        # Create indexes for better query performance
        collection.create_index([("name", ASCENDING)], unique=True)
        collection.create_index([("country", ASCENDING)])
        collection.create_index([("industry", ASCENDING)])
        collection.create_index([("founded_year", DESCENDING)])
        
        print(f"✅ Collection '{collection_name}' created with indexes.")
        return collection
    
    def insert_startups(self, startups: List[Dict[str, Any]], collection_name: str = None):
        """
        Insert startup documents into the collection.
        
        Args:
            startups: List of startup documents
            collection_name: Target collection name
            
        Returns:
            Number of successfully inserted documents
        """
        collection_name = collection_name or config.COLLECTION_NAME
        collection = self.db[collection_name]
        
        inserted_count = 0
        duplicate_count = 0
        
        for startup in startups:
            try:
                collection.insert_one(startup)
                inserted_count += 1
            except DuplicateKeyError:
                duplicate_count += 1
                print(f"⚠️  Duplicate entry skipped: {startup.get('name', 'Unknown')}")
        
        print(f"\n📊 Insertion Summary:")
        print(f"   ✅ Inserted: {inserted_count}")
        print(f"   ⚠️  Duplicates skipped: {duplicate_count}")
        print(f"   📈 Total documents in collection: {collection.count_documents({})}")
        
        return inserted_count
    
    def get_collection_stats(self, collection_name: str = None):
        """
        Get statistics about the collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection statistics
        """
        collection_name = collection_name or config.COLLECTION_NAME
        collection = self.db[collection_name]
        
        stats = {
            'total_documents': collection.count_documents({}),
            'indexes': collection.index_information(),
            'sample_document': collection.find_one()
        }
        
        return stats
    
    def drop_collection(self, collection_name: str = None):
        """
        Drop a collection (use with caution!).
        
        Args:
            collection_name: Name of the collection to drop
        """
        collection_name = collection_name or config.COLLECTION_NAME
        self.db[collection_name].drop()
        print(f"🗑️  Collection '{collection_name}' dropped.")


def load_sample_data():
    """Load sample startup data for testing."""
    sample_startups = [
        {
            "name": "OpenAI",
            "founded_year": 2015,
            "country": "USA",
            "city": "San Francisco",
            "industry": ["AI", "Machine Learning"],
            "funding_rounds": [
                {"round": "Seed", "amount_usd": 120000000, "date": "2015-12-11"},
                {"round": "Series A", "amount_usd": 1000000000, "date": "2019-07-22"}
            ],
            "investors": ["Khosla Ventures", "Microsoft", "Reid Hoffman"],
            "total_funding_usd": 1120000000,
            "employee_count": 500,
            "status": "Operating"
        },
        {
            "name": "Stripe",
            "founded_year": 2010,
            "country": "USA",
            "city": "San Francisco",
            "industry": ["FinTech", "Payments"],
            "funding_rounds": [
                {"round": "Series A", "amount_usd": 2000000, "date": "2011-05-01"},
                {"round": "Series B", "amount_usd": 20000000, "date": "2012-07-01"},
                {"round": "Series C", "amount_usd": 80000000, "date": "2014-01-01"}
            ],
            "investors": ["Sequoia Capital", "Andreessen Horowitz", "Elon Musk"],
            "total_funding_usd": 2200000000,
            "employee_count": 7000,
            "status": "Operating"
        },
        {
            "name": "Revolut",
            "founded_year": 2015,
            "country": "UK",
            "city": "London",
            "industry": ["FinTech", "Banking"],
            "funding_rounds": [
                {"round": "Seed", "amount_usd": 1000000, "date": "2015-07-01"},
                {"round": "Series A", "amount_usd": 10000000, "date": "2016-07-01"},
                {"round": "Series B", "amount_usd": 66000000, "date": "2017-07-01"},
                {"round": "Series C", "amount_usd": 250000000, "date": "2018-04-01"}
            ],
            "investors": ["Index Ventures", "Balderton Capital", "DST Global"],
            "total_funding_usd": 916000000,
            "employee_count": 5000,
            "status": "Operating"
        },
        {
            "name": "Grab",
            "founded_year": 2012,
            "country": "Singapore",
            "city": "Singapore",
            "industry": ["Transportation", "FinTech"],
            "funding_rounds": [
                {"round": "Series A", "amount_usd": 10000000, "date": "2013-01-01"},
                {"round": "Series B", "amount_usd": 90000000, "date": "2014-12-01"},
                {"round": "Series F", "amount_usd": 2500000000, "date": "2018-03-01"}
            ],
            "investors": ["SoftBank", "Toyota", "Microsoft"],
            "total_funding_usd": 12300000000,
            "employee_count": 8000,
            "status": "Operating"
        },
        {
            "name": "Nubank",
            "founded_year": 2013,
            "country": "Brazil",
            "city": "São Paulo",
            "industry": ["FinTech", "Banking"],
            "funding_rounds": [
                {"round": "Series A", "amount_usd": 14600000, "date": "2014-01-01"},
                {"round": "Series B", "amount_usd": 30000000, "date": "2014-10-01"},
                {"round": "Series G", "amount_usd": 400000000, "date": "2019-07-01"}
            ],
            "investors": ["Sequoia Capital", "Tiger Global", "Tencent"],
            "total_funding_usd": 2100000000,
            "employee_count": 4000,
            "status": "Operating"
        }
    ]
    
    return sample_startups


def main():
    """Main function to demonstrate MongoDB setup."""
    print("🚀 Starting MongoDB Atlas Setup...\n")
    
    # Initialize handler
    handler = MongoDBHandler()
    
    # Connect to MongoDB
    if not handler.connect():
        print("❌ Setup failed. Please check your MongoDB URI in .env file.")
        return
    
    # Create collection
    handler.create_collection()
    
    # Load and insert sample data
    print("\n📥 Loading sample startup data...")
    sample_data = load_sample_data()
    handler.insert_startups(sample_data)
    
    # Display collection stats
    print("\n📊 Collection Statistics:")
    stats = handler.get_collection_stats()
    print(f"   Total documents: {stats['total_documents']}")
    print(f"   Indexes: {list(stats['indexes'].keys())}")
    
    # Close connection
    handler.close()
    print("\n✅ Setup complete!")


if __name__ == "__main__":
    main()
