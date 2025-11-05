# Getting Started with Startup Insights

Welcome! This guide will help you get up and running with the Startup Insights MongoDB project in **under 15 minutes**.

## Quick Start (5 minutes)

### 1. Set Up MongoDB Atlas (2 minutes)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) and create a free account
2. Create a free cluster (M0 Sandbox)
3. Add a database user with read/write permissions
4. Whitelist your IP address (or allow access from anywhere for development)
5. Get your connection string

### 2. Configure Environment (1 minute)

```bash
cd /Users/xx/xx/startup-insights-mongodb
cp .env.example .env
```

Edit `.env` and add your MongoDB connection string:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 3. Install Dependencies (1 minute)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Quick Start (1 minute)

```bash
python quick_start.py
```

This will:
- ✅ Verify your setup
- ✅ Connect to MongoDB
- ✅ Create the database and collection
- ✅ Insert sample data
- ✅ Run a basic analysis

## Detailed Walkthrough (15 minutes)

### Step 1: Understand the Project Structure

```
startup-insights-mongodb/
├── Analysis Files
│   ├── data_cleaning.ipynb      # Clean and prepare data
│   ├── analysis.ipynb           # Run aggregation queries
│   └── visualization.ipynb      # Create charts
│
├── Core Scripts
│   ├── mongodb_setup.py         # Database setup
│   ├── config.py                # Configuration
│   └── utils.py                 # Helper functions
│
├── Data
│   ├── data/raw/                # Raw data files
│   └── data/processed/          # Cleaned data
│
└── Documentation
    ├── README.md                # Main documentation
    ├── SETUP_GUIDE.md           # Detailed setup
    └── PROJECT_SUMMARY.md       # Project overview
```

### Step 2: Initialize the Database

```bash
python mongodb_setup.py
```

**What this does:**
- Creates the `startup_insights` database
- Creates the `startups` collection
- Sets up indexes for better performance
- Inserts 5 sample startup records

**Expected output:**
```
Successfully connected to MongoDB Atlas!
Collection 'startups' created with indexes.
Insertion Summary:
   Inserted: 5
   Total documents in collection: 5
```

### Step 3: Explore the Data

Launch Jupyter Notebook:
```bash
jupyter notebook
```

#### A. Data Cleaning (`data_cleaning.ipynb`)

This notebook shows you how to:
- Load data from CSV/JSON files
- Clean and validate data
- Transform data into MongoDB format
- Handle missing values and duplicates

**Run all cells** to see the data cleaning process in action.

#### B. Data Analysis (`analysis.ipynb`)

This notebook contains **6 powerful aggregation queries**:

1. **Top Industries by Funding** - Which sectors attract the most capital?
2. **Geographic Distribution** - Where are the innovation hotspots?
3. **Temporal Trends** - How has startup formation evolved?
4. **Top Funded Startups** - Who are the unicorns?
5. **Industry-Country Analysis** - Regional specializations?
6. **Status Distribution** - Success rates and outcomes?

**Run all cells** to execute all queries and see the results.

#### C. Visualizations (`visualization.ipynb`)

This notebook creates:
- Bar charts for industry analysis
- Choropleth maps for geographic distribution
- Time series charts for trends
- Interactive Plotly visualizations

**Run all cells** to generate all visualizations.

### Step 4: Add Your Own Data

You have three options:

#### Option 1: Load from CSV

```bash
python load_additional_data.py
# Choose option 1
# Enter path to your CSV file
```

Your CSV should have these columns:
```
name,founded_year,country,city,industry,total_funding_usd,employee_count,status
```

#### Option 2: Load from JSON

```bash
python load_additional_data.py
# Choose option 2
# Enter path to your JSON file
```

JSON format:
```json
[
  {
    "name": "YourStartup",
    "founded_year": 2020,
    "country": "USA",
    "city": "San Francisco",
    "industry": ["FinTech", "AI"],
    "total_funding_usd": 5000000,
    "employee_count": 50,
    "status": "Operating"
  }
]
```

#### Option 3: Manual Entry

```bash
python load_additional_data.py
# Choose option 3
# Follow the prompts
```

### Step 5: Run Custom Queries

Open a Python shell or create a new notebook:

```python
from mongodb_setup import MongoDBHandler

# Connect
handler = MongoDBHandler()
handler.connect()
collection = handler.db['startups']

# Example: Find all FinTech startups
fintech = collection.find({"industry": "FinTech"})
for startup in fintech:
    print(f"{startup['name']} - ${startup['total_funding_usd']:,}")

# Example: Aggregate by country
pipeline = [
    {"$group": {
        "_id": "$country",
        "total_funding": {"$sum": "$total_funding_usd"},
        "count": {"$sum": 1}
    }},
    {"$sort": {"total_funding": -1}}
]

results = list(collection.aggregate(pipeline))
for result in results:
    print(f"{result['_id']}: {result['count']} startups, ${result['total_funding']:,}")

handler.close()
```

## Common Tasks

### View All Data

```python
from mongodb_setup import MongoDBHandler

handler = MongoDBHandler()
handler.connect()

startups = list(handler.db['startups'].find({}, {'_id': 0}))
print(f"Found {len(startups)} startups")

for startup in startups:
    print(f"- {startup['name']} ({startup['country']})")

handler.close()
```

### Clear Database

```python
from mongodb_setup import MongoDBHandler

handler = MongoDBHandler()
handler.connect()
handler.drop_collection()  # This deletes all data!
handler.close()
```

### Export Data

```python
import json
from mongodb_setup import MongoDBHandler

handler = MongoDBHandler()
handler.connect()

startups = list(handler.db['startups'].find({}, {'_id': 0}))

with open('export.json', 'w') as f:
    json.dump(startups, f, indent=2)

print(f"Exported {len(startups)} startups to export.json")
handler.close()
```

## Troubleshooting

### "Authentication failed"
- Check your username and password in `.env`
- Verify the database user has correct permissions in MongoDB Atlas

### "Connection timeout"
- Check your IP is whitelisted in Network Access
- Try "Allow access from anywhere" for testing

### "Module not found"
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "No data found"
- Run `python mongodb_setup.py` to insert sample data
- Check connection to MongoDB Atlas

## Learning Resources

- [MongoDB Aggregation Tutorial](https://docs.mongodb.com/manual/aggregation/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)


## You're Ready!

You now have a fully functional startup analytics platform powered by MongoDB Atlas. 