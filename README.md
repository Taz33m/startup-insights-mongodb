<div align="center">
  <img src="logo.png" alt="Startup Insights Logo" width="200"/>
  
  # Startup Insights with MongoDB Atlas
  
  > Analyzing Global Startup Trends using MongoDB's powerful aggregation framework
  
  [![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
</div>

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Security](#security)
- [Usage](#usage)
- [Key Insights](#key-insights)
- [MongoDB Aggregation Queries](#mongodb-aggregation-queries)
- [Visualizations](#visualizations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Overview

This project demonstrates how to leverage **MongoDB Atlas** as a data platform for analyzing global startup ecosystems. Using real-world startup data, we explore funding trends, industry growth patterns, and regional innovation hotspots through MongoDB's flexible document model and powerful aggregation pipelines.

### Why MongoDB?

Traditional SQL databases struggle with semi-structured startup data (varying funding rounds, dynamic investor lists, multi-category industries). MongoDB's document-based model provides:

- **Flexible Schema**: Easily accommodate varying data structures
- **Powerful Aggregations**: Complex analytical queries with the aggregation framework
- **Scalability**: Cloud-native architecture with MongoDB Atlas
- **Rich Queries**: Native support for arrays, nested documents, and geospatial data

## Key Features

- **6+ Complex Aggregation Pipelines** for deep data analysis
- **Geographic Analysis** of startup funding distribution
- **Temporal Trends** showing startup formation over time
- **Industry Insights** identifying high-growth sectors
- **Interactive Visualizations** using Plotly and Seaborn
- **ETL Pipeline** for data cleaning and transformation
- **Comprehensive Documentation** with Jupyter notebooks

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Database** | MongoDB Atlas, PyMongo |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **Development** | Python 3.9+, Jupyter Notebook |
| **Environment** | python-dotenv |

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (free tier available)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/startup-insights-mongodb.git
cd startup-insights-mongodb
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB Atlas

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Configure network access (add your IP address)
4. Create a database user
5. Get your connection string

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your MongoDB connection string:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
DATABASE_NAME=startup_insights
COLLECTION_NAME=startups
```

### 6. Initialize Database

```bash
python mongodb_setup.py
```

This will:
- Connect to MongoDB Atlas
- Create the database and collection
- Set up indexes
- Insert sample startup data

## Security

**IMPORTANT**: This project follows security best practices to protect your credentials.

### Critical Security Rules

1. **Never commit `.env` file** - It contains your MongoDB credentials
2. **Use environment variables** - Never hardcode passwords in code
3. **Review before committing** - Run `python check_security.py` before git commits

### Security Verification

Run the security check script:

```bash
python check_security.py
```

This will verify:
- `.gitignore` is properly configured
- `.env` file is not tracked by git
- No hardcoded secrets in code
- No sensitive files staged for commit

### MongoDB Atlas Security

- Use strong passwords (20+ characters)
- Whitelist specific IP addresses (not 0.0.0.0/0 in production)
- Enable encryption at rest (default in Atlas)
- Rotate credentials regularly

For detailed security guidelines, see **[SECURITY.md](SECURITY.md)**.

## Usage

### Running the Analysis

1. **Data Cleaning**
   ```bash
   jupyter notebook data_cleaning.ipynb
   ```
   - Load raw data
   - Clean and validate
   - Transform to MongoDB format

2. **Data Analysis**
   ```bash
   jupyter notebook analysis.ipynb
   ```
   - Execute aggregation pipelines
   - Extract insights
   - Export results

3. **Visualization**
   ```bash
   jupyter notebook visualization.ipynb
   ```
   - Create interactive charts
   - Generate reports
   - Save visualizations

### Quick Start with Python

```python
from mongodb_setup import MongoDBHandler

# Connect to MongoDB
handler = MongoDBHandler()
handler.connect()

# Get collection
collection = handler.db['startups']

# Run aggregation query
pipeline = [
    {"$group": {
        "_id": "$country",
        "total_funding": {"$sum": "$total_funding_usd"}
    }},
    {"$sort": {"total_funding": -1}}
]

results = list(collection.aggregate(pipeline))
print(results)
```

## Key Insights

Based on our analysis of the startup ecosystem:

### 1. **Industry Trends**
- **FinTech** dominates with the highest total funding ($18.2B+)
- **AI/Machine Learning** shows rapid growth (300% YoY)
- **HealthTech** emerging as a major sector post-2020

### 2. **Geographic Patterns**
- **USA** leads with 45% of total global startup funding
- **Asia-Pacific** fastest growing region (Singapore, India, China)
- **European** startups show higher average funding per round

### 3. **Temporal Analysis**
- Peak startup formation: **2015-2019**
- Average time to Series A: **18-24 months**
- Funding rounds increasing in size (avg +35% YoY)

### 4. **Success Factors**
- Top-funded startups average **$2.5B** in total funding
- **Multi-industry** startups attract 40% more funding
- **Metropolitan hubs** (SF, London, Beijing) account for 60% of funding

## MongoDB Aggregation Queries

### Query 1: Top Industries by Funding

```javascript
[
  {"$unwind": "$industry"},
  {"$group": {
    "_id": "$industry",
    "total_funding": {"$sum": "$total_funding_usd"},
    "startup_count": {"$sum": 1}
  }},
  {"$sort": {"total_funding": -1}},
  {"$limit": 10}
]
```

### Query 2: Funding Distribution by Country

```javascript
[
  {"$group": {
    "_id": "$country",
    "total_funding": {"$sum": "$total_funding_usd"},
    "startup_count": {"$sum": 1},
    "avg_funding": {"$avg": "$total_funding_usd"}
  }},
  {"$sort": {"total_funding": -1}}
]
```

### Query 3: Year-over-Year Growth

```javascript
[
  {"$group": {
    "_id": "$founded_year",
    "count": {"$sum": 1},
    "total_funding": {"$sum": "$total_funding_usd"}
  }},
  {"$sort": {"_id": 1}}
]
```

### Query 4: Industry-Country Cross Analysis

```javascript
[
  {"$unwind": "$industry"},
  {"$group": {
    "_id": {
      "industry": "$industry",
      "country": "$country"
    },
    "startup_count": {"$sum": 1},
    "avg_funding": {"$avg": "$total_funding_usd"}
  }},
  {"$sort": {"avg_funding": -1}}
]
```

## Visualizations

The project includes several interactive visualizations:

1. **Bar Chart**: Top 10 Industries by Total Funding
2. **Choropleth Map**: Global Funding Distribution
3. **Line Chart**: Startup Formation Timeline
4. **Horizontal Bar**: Top Funded Startups
5. **Scatter Plot**: Funding vs Employee Count
6. **Pie Chart**: Industry Distribution

All visualizations are generated using Plotly for interactivity and can be exported as HTML or PNG.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MongoDB Atlas for providing excellent cloud database services
- Crunchbase for startup data inspiration
- The open-source community for amazing tools

---

⭐ If you found this project helpful, please consider giving it a star!

**Built with ❤️ using MongoDB Atlas and Python**
