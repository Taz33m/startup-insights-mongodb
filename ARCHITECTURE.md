## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Jupyter    │  │   Python     │  │   Terminal   │          │
│  │  Notebooks   │  │   Scripts    │  │   Commands   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Python Application                       │ │
│  │                                                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │   config.py  │  │   utils.py   │  │ mongodb_     │    │ │
│  │  │              │  │              │  │ setup.py     │    │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │              Data Processing Layer                    │ │ │
│  │  │                                                        │ │ │
│  │  │  • Pandas (Data Manipulation)                        │ │ │
│  │  │  • NumPy (Numerical Operations)                      │ │ │
│  │  │  • PyMongo (MongoDB Driver)                          │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │            Visualization Layer                        │ │ │
│  │  │                                                        │ │ │
│  │  │  • Plotly (Interactive Charts)                       │ │ │
│  │  │  • Seaborn (Statistical Plots)                       │ │ │
│  │  │  • Matplotlib (Base Plotting)                        │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   MongoDB Atlas                             │ │
│  │                   (Cloud Database)                          │ │
│  │                                                             │ │
│  │  Database: startup_insights                                │ │
│  │  Collection: startups                                      │ │
│  │                                                             │ │
│  │  Indexes:                                                  │ │
│  │  • name (unique)                                           │ │
│  │  • country                                                 │ │
│  │  • industry                                                │ │
│  │  • founded_year (desc)                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────┐
│  Raw Data   │
│  (CSV/JSON) │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Data Cleaning      │
│  (Pandas)           │
│  • Validate         │
│  • Transform        │
│  • Normalize        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  MongoDB Insert     │
│  (PyMongo)          │
│  • Connection       │
│  • Validation       │
│  • Insertion        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  MongoDB Atlas      │
│  (Storage)          │
│  • Documents        │
│  • Indexes          │
│  • Replication      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Aggregation        │
│  (Pipelines)        │
│  • Group            │
│  • Sort             │
│  • Project          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Analysis Results   │
│  (Pandas DataFrame) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Visualizations     │
│  (Plotly/Seaborn)   │
│  • Charts           │
│  • Graphs           │
│  • Maps             │
└─────────────────────┘
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                    Jupyter Notebooks                          │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐│
│  │ data_cleaning   │  │   analysis      │  │visualization ││
│  │    .ipynb       │  │    .ipynb       │  │   .ipynb     ││
│  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘│
│           │                    │                    │        │
└───────────┼────────────────────┼────────────────────┼────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌───────────────────────────────────────────────────────────────┐
│                     Core Python Modules                        │
│                                                                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  config.py   │◄───┤mongodb_setup │◄───┤   utils.py   │   │
│  │              │    │    .py       │    │              │   │
│  └──────────────┘    └──────┬───────┘    └──────────────┘   │
│                             │                                 │
└─────────────────────────────┼─────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  MongoDB Atlas   │
                    │   (Database)     │
                    └──────────────────┘
```

## File Dependencies

```
mongodb_setup.py
├── config.py (environment variables)
├── pymongo (database connection)
└── utils.py (helper functions)

data_cleaning.ipynb
├── pandas (data manipulation)
├── config.py (paths)
└── utils.py (validation)

analysis.ipynb
├── mongodb_setup.py (database handler)
├── pymongo (aggregation)
└── pandas (results processing)

visualization.ipynb
├── mongodb_setup.py (data access)
├── plotly (interactive charts)
└── seaborn (statistical plots)

quick_start.py
├── mongodb_setup.py (setup functions)
└── utils.py (statistics)

load_additional_data.py
├── mongodb_setup.py (insertion)
├── pandas (CSV processing)
└── config.py (paths)
```

## Aggregation Pipeline Flow

```
MongoDB Collection
       │
       ▼
┌─────────────┐
│  $unwind    │  Deconstruct arrays
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   $match    │  Filter documents
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   $group    │  Group and aggregate
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   $sort     │  Sort results
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  $project   │  Shape output
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   $limit    │  Limit results
└──────┬──────┘
       │
       ▼
    Results
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│  Jupyter Notebook, Plotly, Seaborn, Matplotlib         │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  Python 3.9+, Pandas, NumPy                            │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   Data Access Layer                      │
│  PyMongo, MongoDB Driver                                │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   Database Layer                         │
│  MongoDB Atlas (Cloud)                                  │
└─────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Application                            │
│                                                          │
│  ┌────────────┐                                         │
│  │ .env file  │  (Not in version control)              │
│  │ • URI      │                                         │
│  │ • Secrets  │                                         │
│  └────────────┘                                         │
└────────────┬────────────────────────────────────────────┘
             │
             │ Encrypted Connection (TLS/SSL)
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│                MongoDB Atlas                             │
│                                                          │
│  ┌──────────────────────────────────────────┐          │
│  │  Security Features:                       │          │
│  │  • Authentication (Username/Password)     │          │
│  │  • IP Whitelist                          │          │
│  │  • Encryption at Rest                    │          │
│  │  • Encryption in Transit                 │          │
│  │  • Role-Based Access Control             │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

## Deployment Options

### Local Development
```
Developer Machine
├── Python Virtual Environment
├── Jupyter Notebook Server
├── Local Code Execution
└── MongoDB Atlas (Cloud)
```

### Cloud Deployment (Future)
```
Cloud Platform (AWS/GCP/Azure)
├── Container (Docker)
├── Web Application (Streamlit/Dash)
├── API Server (FastAPI/Flask)
└── MongoDB Atlas (Cloud)
```

## Scalability Considerations

```
Current Architecture:
┌──────────────┐
│ Single User  │
│ Local Python │
│ MongoDB Free │
└──────────────┘

Scalable Architecture:
┌──────────────────────────────────┐
│ Multiple Users                    │
│ Web Application (Streamlit)       │
│ MongoDB Cluster (Sharded)         │
│ Caching Layer (Redis)             │
│ Load Balancer                     │
└──────────────────────────────────┘
```

## Monitoring & Observability

```
┌─────────────────────────────────────┐
│  MongoDB Atlas Dashboard             │
│  • Query Performance                 │
│  • Index Usage                       │
│  • Connection Pool                   │
│  • Storage Metrics                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Application Logging                 │
│  • Python logging module             │
│  • Error tracking                    │
│  • Performance metrics               │
└─────────────────────────────────────┘
```

---

**Architecture Version**: 1.0  
**Last Updated**: 2024-11-04  
**Status**: Production Ready
