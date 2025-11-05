# Data Schema Documentation

This document describes the data structure used in the Startup Insights MongoDB project.

## Collection: `startups`

### Document Structure

```javascript
{
  "name": String,              // Required, Unique
  "founded_year": Integer,     // Required
  "country": String,           // Required
  "city": String,              // Optional
  "industry": [String],        // Array of industry tags
  "funding_rounds": [          // Optional array of funding rounds
    {
      "round": String,         // e.g., "Seed", "Series A", "Series B"
      "amount_usd": Number,    // Funding amount in USD
      "date": String           // ISO date format "YYYY-MM-DD"
    }
  ],
  "investors": [String],       // Optional array of investor names
  "total_funding_usd": Number, // Total funding raised
  "employee_count": Integer,   // Number of employees
  "status": String             // "Operating", "Acquired", "Closed", etc.
}
```

## Field Descriptions

### Required Fields

#### `name` (String)
- **Description**: Official company name
- **Constraints**: Unique, non-empty
- **Example**: `"OpenAI"`
- **Index**: Yes (unique)

#### `founded_year` (Integer)
- **Description**: Year the company was founded
- **Constraints**: 1900 <= year <= current year
- **Example**: `2015`
- **Index**: Yes (descending)

#### `country` (String)
- **Description**: Country where company is headquartered
- **Constraints**: Valid country name
- **Example**: `"USA"`, `"UK"`, `"Singapore"`
- **Index**: Yes

#### `total_funding_usd` (Number)
- **Description**: Total funding raised in USD
- **Constraints**: >= 0
- **Example**: `1120000000` (1.12 billion)
- **Format**: Integer or float

#### `status` (String)
- **Description**: Current operational status
- **Allowed Values**: 
  - `"Operating"` - Currently active
  - `"Acquired"` - Bought by another company
  - `"Closed"` - No longer operating
  - `"IPO"` - Publicly traded
- **Example**: `"Operating"`

### Optional Fields

#### `city` (String)
- **Description**: City where company is headquartered
- **Example**: `"San Francisco"`, `"London"`
- **Default**: `null`

#### `industry` (Array of Strings)
- **Description**: Industry categories/tags
- **Example**: `["AI", "Machine Learning"]`
- **Common Values**:
  - `"FinTech"`
  - `"AI"`
  - `"HealthTech"`
  - `"EdTech"`
  - `"SaaS"`
  - `"E-commerce"`
  - `"CleanTech"`
- **Index**: Yes
- **Default**: `[]`

#### `funding_rounds` (Array of Objects)
- **Description**: Detailed funding history
- **Example**:
  ```json
  [
    {
      "round": "Seed",
      "amount_usd": 1000000,
      "date": "2015-06-01"
    },
    {
      "round": "Series A",
      "amount_usd": 10000000,
      "date": "2017-03-15"
    }
  ]
  ```
- **Round Types**:
  - `"Seed"`
  - `"Series A"`, `"Series B"`, `"Series C"`, etc.
  - `"Bridge"`
  - `"IPO"`
- **Default**: `[]`

#### `investors` (Array of Strings)
- **Description**: List of investor names
- **Example**: `["Sequoia Capital", "Andreessen Horowitz"]`
- **Default**: `[]`

#### `employee_count` (Integer)
- **Description**: Current number of employees
- **Constraints**: >= 0
- **Example**: `500`
- **Default**: `0`

## Sample Documents

### Minimal Document

```json
{
  "name": "MinimalStartup",
  "founded_year": 2020,
  "country": "USA",
  "industry": ["SaaS"],
  "total_funding_usd": 0,
  "employee_count": 5,
  "status": "Operating"
}
```

### Complete Document

```json
{
  "name": "OpenAI",
  "founded_year": 2015,
  "country": "USA",
  "city": "San Francisco",
  "industry": ["AI", "Machine Learning"],
  "funding_rounds": [
    {
      "round": "Seed",
      "amount_usd": 120000000,
      "date": "2015-12-11"
    },
    {
      "round": "Series A",
      "amount_usd": 1000000000,
      "date": "2019-07-22"
    }
  ],
  "investors": [
    "Khosla Ventures",
    "Microsoft",
    "Reid Hoffman"
  ],
  "total_funding_usd": 1120000000,
  "employee_count": 500,
  "status": "Operating"
}
```

## Indexes

The collection has the following indexes for optimal query performance:

```javascript
// Unique index on name
db.startups.createIndex({ "name": 1 }, { unique: true })

// Index on country for geographic queries
db.startups.createIndex({ "country": 1 })

// Multi-key index on industry array
db.startups.createIndex({ "industry": 1 })

// Descending index on founded_year for temporal queries
db.startups.createIndex({ "founded_year": -1 })
```

## Data Validation

### Python Validation Example

```python
def validate_startup(startup: dict) -> bool:
    """Validate startup document."""
    
    # Required fields
    required = ['name', 'founded_year', 'country', 'total_funding_usd', 'status']
    if not all(field in startup for field in required):
        return False
    
    # Type checks
    if not isinstance(startup['name'], str) or not startup['name']:
        return False
    
    if not isinstance(startup['founded_year'], int):
        return False
    
    if startup['founded_year'] < 1900 or startup['founded_year'] > 2024:
        return False
    
    if not isinstance(startup['total_funding_usd'], (int, float)):
        return False
    
    if startup['total_funding_usd'] < 0:
        return False
    
    # Valid status values
    valid_statuses = ['Operating', 'Acquired', 'Closed', 'IPO']
    if startup['status'] not in valid_statuses:
        return False
    
    return True
```

## Common Query Patterns

### Find by Industry

```javascript
db.startups.find({ "industry": "FinTech" })
```

### Find by Country and Funding Range

```javascript
db.startups.find({
  "country": "USA",
  "total_funding_usd": { "$gte": 1000000, "$lte": 10000000 }
})
```

### Find Recent Startups

```javascript
db.startups.find({
  "founded_year": { "$gte": 2020 }
}).sort({ "founded_year": -1 })
```

### Find by Multiple Industries

```javascript
db.startups.find({
  "industry": { "$in": ["AI", "Machine Learning"] }
})
```

## Data Import/Export

### Export to JSON

```bash
mongoexport --uri="mongodb+srv://..." \
  --collection=startups \
  --out=startups_export.json \
  --jsonArray
```

### Import from JSON

```bash
mongoimport --uri="mongodb+srv://..." \
  --collection=startups \
  --file=startups_import.json \
  --jsonArray
```

### Export to CSV

```bash
mongoexport --uri="mongodb+srv://..." \
  --collection=startups \
  --type=csv \
  --fields=name,founded_year,country,total_funding_usd,status \
  --out=startups_export.csv
```

## Best Practices

1. **Always validate data** before insertion
2. **Use consistent naming** for industries and countries
3. **Store dates in ISO format** (YYYY-MM-DD)
4. **Keep funding amounts in USD** for consistency
5. **Update total_funding_usd** when adding funding rounds
6. **Use arrays for multi-valued fields** (industry, investors)
7. **Index frequently queried fields**
8. **Avoid deeply nested documents** (max 2-3 levels)

## Data Sources

Recommended sources for startup data:

- **Crunchbase** - Comprehensive startup database
- **PitchBook** - Private market data
- **AngelList** - Startup and investor profiles
- **CB Insights** - Market intelligence
- **Kaggle** - Public datasets
- **StartupBlink** - Global startup ecosystem map

## Extending the Schema

To add new fields:

1. **Update this documentation**
2. **Add validation** in `mongodb_setup.py`
3. **Update notebooks** to handle new fields
4. **Consider adding indexes** if frequently queried
5. **Maintain backward compatibility**

Example extension:

```json
{
  // ... existing fields ...
  "website": "https://example.com",
  "description": "Brief company description",
  "tags": ["B2B", "Enterprise"],
  "valuation_usd": 1000000000,
  "last_funding_date": "2023-06-15"
}
```

---

**Last Updated**: 2024-11-04  
**Schema Version**: 1.0
