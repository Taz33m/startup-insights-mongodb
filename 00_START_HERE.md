# START HERE - Startup Insights MongoDB Project

Welcome to the **Startup Insights with MongoDB Atlas** project! This document will guide you through everything you need to know.

## ⚡ 5-Minute Quick Start

```bash
# 1. Navigate to project
cd /Users/xx/xx/startup-insights-mongodb

# 2. Set up environment
cp .env.example .env
# Edit .env with your MongoDB Atlas connection string

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Run quick start
python quick_start.py

# 5. Launch Jupyter
jupyter notebook
```

## What This Project Does

This project demonstrates:

1. **MongoDB Atlas Integration** - Cloud database setup and connection
2. **Data Engineering** - ETL pipeline for startup data
3. **Advanced Queries** - 6+ MongoDB aggregation pipelines
4. **Data Analysis** - Insights about global startup ecosystems
5. **Visualization** - Interactive charts and geographic maps
6. **Best Practices** - Clean code, documentation, and modularity

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Database** | MongoDB Atlas (Cloud) |
| **Language** | Python 3.9+ |
| **Database Driver** | PyMongo 4.6+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **Development** | Jupyter Notebook |
| **Environment** | python-dotenv |

## Key Features

### 6 MongoDB Aggregation Queries

1. **Top Industries by Funding** - Which sectors attract the most capital?
2. **Geographic Distribution** - Where are the innovation hotspots?
3. **Temporal Trends** - How has startup formation evolved?
4. **Top Funded Startups** - Who are the unicorns?
5. **Industry-Country Analysis** - Regional specializations?
6. **Status Distribution** - Success rates and outcomes?

### 6 Data Visualizations

1. Bar Chart - Top 10 Industries
2. Choropleth Map - Global Funding
3. Time Series - Formation Timeline
4. Horizontal Bar - Top Funded Startups
5. Scatter Plot - Funding vs Employees
6. Pie Chart - Industry Distribution