#!/usr/bin/env python3
"""
Script to load additional startup data from various sources.
Supports CSV, JSON, and manual data entry.
"""
import json
import pandas as pd
from mongodb_setup import MongoDBHandler
import config


def load_from_csv(filepath: str):
    """
    Load startup data from CSV file.
    
    Expected CSV columns:
    - name, founded_year, country, city, industry, total_funding_usd, employee_count, status
    """
    print(f"📥 Loading data from {filepath}...")
    
    df = pd.read_csv(filepath)
    
    # Convert industry string to list
    if 'industry' in df.columns:
        df['industry'] = df['industry'].apply(
            lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) else []
        )
    
    # Convert to list of dictionaries
    startups = df.to_dict('records')
    
    print(f"✅ Loaded {len(startups)} startups from CSV")
    return startups


def load_from_json(filepath: str):
    """Load startup data from JSON file."""
    print(f"📥 Loading data from {filepath}...")
    
    with open(filepath, 'r') as f:
        startups = json.load(f)
    
    print(f"✅ Loaded {len(startups)} startups from JSON")
    return startups


def create_startup_interactive():
    """Interactive CLI for creating a startup entry."""
    print("\n" + "="*60)
    print("📝 CREATE NEW STARTUP ENTRY")
    print("="*60 + "\n")
    
    startup = {}
    
    # Basic info
    startup['name'] = input("Company Name: ").strip()
    startup['founded_year'] = int(input("Founded Year: ").strip())
    startup['country'] = input("Country: ").strip()
    startup['city'] = input("City: ").strip()
    
    # Industry (comma-separated)
    industries = input("Industries (comma-separated): ").strip()
    startup['industry'] = [i.strip() for i in industries.split(',')]
    
    # Funding
    funding = input("Total Funding (USD): ").strip()
    startup['total_funding_usd'] = float(funding) if funding else 0
    
    # Employees
    employees = input("Employee Count: ").strip()
    startup['employee_count'] = int(employees) if employees else 0
    
    # Status
    startup['status'] = input("Status (Operating/Acquired/Closed): ").strip() or "Operating"
    
    print("\n✅ Startup entry created!")
    print(json.dumps(startup, indent=2))
    
    return startup


def main():
    """Main function."""
    print("\n" + "="*60)
    print("📊 LOAD ADDITIONAL STARTUP DATA")
    print("="*60 + "\n")
    
    print("Choose data source:")
    print("1. CSV file")
    print("2. JSON file")
    print("3. Manual entry")
    print("4. Load sample data from data/raw/")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    startups = []
    
    if choice == '1':
        filepath = input("Enter CSV file path: ").strip()
        try:
            startups = load_from_csv(filepath)
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return
    
    elif choice == '2':
        filepath = input("Enter JSON file path: ").strip()
        try:
            startups = load_from_json(filepath)
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return
    
    elif choice == '3':
        while True:
            startup = create_startup_interactive()
            startups.append(startup)
            
            more = input("\nAdd another startup? (y/n): ").strip().lower()
            if more != 'y':
                break
    
    elif choice == '4':
        import os
        sample_file = os.path.join(config.RAW_DATA_DIR, 'sample_startups.json')
        try:
            startups = load_from_json(sample_file)
        except Exception as e:
            print(f"❌ Error loading sample data: {e}")
            return
    
    else:
        print("❌ Invalid choice")
        return
    
    if not startups:
        print("⚠️  No data to insert")
        return
    
    # Insert into MongoDB
    print(f"\n📤 Inserting {len(startups)} startups into MongoDB...")
    
    handler = MongoDBHandler()
    if not handler.connect():
        print("❌ Failed to connect to MongoDB")
        return
    
    try:
        inserted = handler.insert_startups(startups)
        print(f"\n✅ Successfully inserted {inserted} startups!")
        
        # Show updated stats
        stats = handler.get_collection_stats()
        print(f"📊 Total startups in database: {stats['total_documents']}")
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    
    finally:
        handler.close()


if __name__ == "__main__":
    main()
