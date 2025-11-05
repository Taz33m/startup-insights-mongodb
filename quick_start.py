#!/usr/bin/env python3
"""
Quick start script to verify setup and run basic analysis.
"""
import os
import sys
from mongodb_setup import MongoDBHandler, load_sample_data
from utils import calculate_funding_stats, format_currency


def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment setup...\n")
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please copy .env.example to .env and configure your MongoDB URI")
        return False
    
    # Check MongoDB URI
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri or '<password>' in mongodb_uri:
        print("❌ MongoDB URI not configured!")
        print("   Please update MONGODB_URI in .env file")
        return False
    
    print("✅ Environment configured correctly\n")
    return True


def test_connection():
    """Test MongoDB connection."""
    print("🔌 Testing MongoDB connection...\n")
    
    handler = MongoDBHandler()
    if handler.connect():
        print("✅ Successfully connected to MongoDB Atlas!\n")
        handler.close()
        return True
    else:
        print("❌ Failed to connect to MongoDB")
        print("   Please check your connection string and network access")
        return False


def setup_database():
    """Initialize database with sample data."""
    print("📊 Setting up database...\n")
    
    handler = MongoDBHandler()
    handler.connect()
    
    # Create collection
    handler.create_collection()
    
    # Load sample data
    sample_data = load_sample_data()
    
    # Insert data
    handler.insert_startups(sample_data)
    
    # Show stats
    stats = handler.get_collection_stats()
    print(f"\n📈 Database ready with {stats['total_documents']} startups")
    
    handler.close()
    return True


def run_sample_analysis():
    """Run a sample analysis."""
    print("\n" + "="*60)
    print("📊 SAMPLE ANALYSIS")
    print("="*60 + "\n")
    
    handler = MongoDBHandler()
    handler.connect()
    
    collection = handler.db['startups']
    
    # Get all startups
    startups = list(collection.find({}, {'_id': 0}))
    
    if not startups:
        print("⚠️  No data found. Run setup first.")
        handler.close()
        return
    
    # Calculate stats
    stats = calculate_funding_stats(startups)
    
    print(f"🏢 Total Startups: {len(startups)}")
    print(f"💰 Total Funding: {format_currency(stats['total'])}")
    print(f"📈 Average Funding: {format_currency(stats['average'])}")
    print(f"🎯 Max Funding: {format_currency(stats['max'])}")
    print(f"📉 Min Funding: {format_currency(stats['min'])}")
    
    # Top 3 funded startups
    print("\n🏆 Top 3 Most Funded Startups:")
    top_startups = sorted(startups, key=lambda x: x.get('total_funding_usd', 0), reverse=True)[:3]
    
    for i, startup in enumerate(top_startups, 1):
        funding = format_currency(startup.get('total_funding_usd', 0))
        print(f"   {i}. {startup['name']} ({startup['country']}) - {funding}")
    
    # Countries
    countries = {}
    for startup in startups:
        country = startup.get('country', 'Unknown')
        countries[country] = countries.get(country, 0) + 1
    
    print(f"\n🌍 Countries Represented: {len(countries)}")
    for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
        print(f"   {country}: {count} startup{'s' if count > 1 else ''}")
    
    print("\n" + "="*60)
    
    handler.close()


def main():
    """Main function."""
    print("\n" + "="*60)
    print("🚀 STARTUP INSIGHTS - QUICK START")
    print("="*60 + "\n")
    
    # Step 1: Check environment
    if not check_environment():
        print("\n❌ Setup incomplete. Please follow SETUP_GUIDE.md")
        sys.exit(1)
    
    # Step 2: Test connection
    if not test_connection():
        print("\n❌ Connection failed. Please check your MongoDB configuration")
        sys.exit(1)
    
    # Step 3: Setup database
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Database setup failed: {e}")
        sys.exit(1)
    
    # Step 4: Run sample analysis
    try:
        run_sample_analysis()
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        sys.exit(1)
    
    # Success message
    print("\n✅ Quick start completed successfully!")
    print("\n📚 Next Steps:")
    print("   1. Open Jupyter: jupyter notebook")
    print("   2. Explore data_cleaning.ipynb")
    print("   3. Run analysis.ipynb")
    print("   4. Create visualizations in visualization.ipynb")
    print("\n🎉 Happy analyzing!\n")


if __name__ == "__main__":
    main()
