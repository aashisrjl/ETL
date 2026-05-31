# ETL Pipeline - Data Warehouse & Mining Assignment 1

A complete **Extract, Transform, Load (ETL)** pipeline for building a sports booking data warehouse. This project extracts data from multiple sources (CSV, Excel, and APIs), transforms it using dimensional modeling, and loads it into a PostgreSQL database.

## 📊 Project Overview

This ETL pipeline implements a **star schema** design for analytical queries on booking data. It integrates data from:
- **CSV Files** - Booking transactions
- **Excel Files** - Sports grounds master data
- **REST APIs** - User information from JSONPlaceholder

The processed data is loaded into a PostgreSQL data warehouse for OLAP analytics.

---

## 🔄 ETL Pipeline Architecture

```
┌──────────────────────────────────────────┐
│       DATA SOURCES                       │
│  • CSV (bookings.csv)                    │
│  • Excel (grounds.xlsx)                  │
│  • APIs (JSONPlaceholder users)          │
└──────────────┬──────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│       EXTRACT (extract.py)               │
│  Extract data from all sources           │
│  Output: 3 DataFrames                    │
└──────────────┬──────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│      TRANSFORM (transform.py)            │
│  • Data cleaning & validation            │
│  • Dimensional modeling:                 │
│    - dim_users                           │
│    - dim_grounds                         │
│    - dim_date                            │
│    - fact_bookings                       │
└──────────────┬──────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│       LOAD (load.py)                     │
│  Load transformed data to PostgreSQL     │
│  Create schema from schema.sql           │
└──────────────┬──────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│    PostgreSQL Data Warehouse             │
│         etl_warehouse DB                 │
└──────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Assignment1-ETL/
├── main.ipynb                 # Main ETL orchestration notebook
├── README.md                  # This file
├── requirements.txt           # Python dependencies
│
├── config/
│   ├── __init__.py
│   ├── db_config.py           # PostgreSQL connection setup
│   └── db_config.ipynb        # Database config notebook
│
├── data/
│   ├── raw/                   # Raw input data
│   │   ├── bookings.csv       # Booking transactions
│   │   ├── grounds.xlsx       # Sports grounds data
│   │   └── users_api.json     # API response cache
│   └── processed/             # Output data (post-ETL)
│
├── db/
│   └── schema.sql             # PostgreSQL schema (DDL)
│
├── etl/                       # Jupyter Notebooks (interactive)
│   ├── __init__.py
│   ├── extract.ipynb
│   ├── transform.ipynb
│   └── load.ipynb
│
├── etl_py/                    # Python modules (production)
│   ├── __init__.py
│   ├── extract.py             # Extract from CSV/Excel/APIs
│   ├── transform.py           # Transform & dimensional modeling
│   └── load.py                # Load to PostgreSQL
│
└── etlenv/                    # Python virtual environment
    ├── bin/
    ├── lib/
    └── share/
```

---

## 🔍 Pipeline Stages

### **1. Extract** (`etl_py/extract.py`)

Retrieves data from all three sources:

| Source | Function | Output |
|--------|----------|--------|
| **CSV** | `extract_data()` | `df_bookings` |
| **Excel** | `extract_data()` | `df_grounds` |
| **API** | `users_data()` | `df_users` |

**Key Functions:**
- `users_data()` - Fetches user data from JSONPlaceholder API
- `extract_data()` - Combines all three data sources

**Input Data:**
- `data/raw/bookings.csv` - Booking records with user, ground, date, time, and price
- `data/raw/grounds.xlsx` - Sports facility information
- JSONPlaceholder API (https://jsonplaceholder.typicode.com/users)

---

### **2. Transform** (`etl_py/transform.py`)

Applies data cleaning and builds a **dimensional model** (star schema):

| Table | Type | Source | Description |
|-------|------|--------|-------------|
| **dim_users** | Dimension | df_users | User profiles (ID, name, email, location) |
| **dim_grounds** | Dimension | df_grounds | Sports facility master data |
| **dim_date** | Dimension | df_bookings | Time dimension for temporal analysis |
| **fact_bookings** | Fact | df_bookings | Booking transactions (measures & foreign keys) |

**Key Functions:**
- `build_dim_users()` - Creates user dimension with ID alignment
- `build_dim_grounds()` - Creates facility dimension
- `build_dim_date()` - Extracts date components for time-based analysis
- `build_fact_bookings()` - Creates fact table with foreign keys

**Data Cleaning:**
- Duplicate removal
- ID alignment and normalization
- Data type standardization
- NULL/missing value handling

---

### **3. Load** (`etl_py/load.py`)

Loads transformed data into PostgreSQL:

| Function | Purpose |
|----------|---------|
| `_ensure_schema()` | Creates tables from `db/schema.sql` |
| `load_data()` | Inserts dimension and fact tables using SQLAlchemy |

**Target Database:**
- Host: `localhost` (configurable)
- Database: `etl_warehouse`
- Tables: 4 (3 dimensions + 1 fact)

---

## 🗄️ Database Schema

### Dimension Tables

#### `dim_users`
```sql
user_id (PK)        INT PRIMARY KEY
name                VARCHAR(100)
username            VARCHAR(100)
email               VARCHAR(150)
phone               VARCHAR(50)
website             VARCHAR(100)
city                VARCHAR(100)
company             VARCHAR(150)
created_at          TIMESTAMP (auto)
```

#### `dim_grounds`
```sql
ground_id (PK)      INT PRIMARY KEY
ground_name         VARCHAR(150)
location            VARCHAR(150)
ground_type         VARCHAR(100)
price_per_hour      NUMERIC(10,2)
is_active           BOOLEAN
created_at          TIMESTAMP (auto)
```

#### `dim_date`
```sql
date_id (PK)        SERIAL PRIMARY KEY
full_date           DATE (UNIQUE)
day                 INT
month               INT
year                INT
quarter             INT
weekday             INT
weekday_name        VARCHAR(20)
```

### Fact Table

#### `fact_bookings`
```sql
booking_id (PK)     INT PRIMARY KEY
user_id (FK)        INT → dim_users(user_id)
ground_id (FK)      INT → dim_grounds(ground_id)
date_id (FK)        INT → dim_date(date_id)
booking_date        DATE
slot_time           VARCHAR(50)
duration_hours      NUMERIC(5,2)
total_price         NUMERIC(10,2)
booking_status      VARCHAR(50)
created_at          TIMESTAMP (auto)
```

---

## 🛠️ Technologies & Dependencies

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.8+ |
| **Database** | PostgreSQL |
| **Data Processing** | Pandas, NumPy |
| **APIs** | Requests |
| **Excel** | OpenPyXL, xlrd |
| **ORM** | SQLAlchemy |
| **DB Driver** | psycopg2-binary |
| **Config** | python-dotenv |
| **Testing** | pytest, black, flake8, pylint |

See `requirements.txt` for complete dependencies.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Assignment1-ETL
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv etlenv
source etlenv/bin/activate  # On Windows: etlenv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Connection

Create a `.env` file in the project root:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_warehouse
DB_USER=postgres
DB_PASSWORD=your_password
```

Alternatively, update `config/db_config.py` with your PostgreSQL credentials.

### Step 5: Create PostgreSQL Database
```bash
createdb etl_warehouse
```

---

## ▶️ Running the ETL Pipeline

### Option 1: Run Python Modules (Production)

```bash
# Activate virtual environment
source etlenv/bin/activate

# Run the main ETL script
python main.py
```

### Option 2: Run Jupyter Notebooks (Interactive)

```bash
# Start Jupyter
jupyter notebook

# Open main.ipynb and run cells in order:
# 1. extract.ipynb
# 2. transform.ipynb
# 3. load.ipynb
```

### Expected Output
```
PostgreSQL connection successful
Loading dim_users with 10 rows ...
Loading dim_grounds with 5 rows ...
Loading dim_date with 30 rows ...
Loading fact_bookings with 100 rows ...
All tables loaded successfully.
```

---

## 📊 Querying the Warehouse

After the ETL completes, query your data warehouse:

### Total Bookings by User
```sql
SELECT u.name, COUNT(f.booking_id) as total_bookings
FROM fact_bookings f
JOIN dim_users u ON f.user_id = u.user_id
GROUP BY u.name
ORDER BY total_bookings DESC;
```

### Revenue by Ground
```sql
SELECT g.ground_name, SUM(f.total_price) as total_revenue
FROM fact_bookings f
JOIN dim_grounds g ON f.ground_id = g.ground_id
GROUP BY g.ground_name
ORDER BY total_revenue DESC;
```

### Bookings by Month
```sql
SELECT d.year, d.month, COUNT(*) as booking_count
FROM fact_bookings f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

---

## 🔧 Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running: `pg_isready`
- Check credentials in `.env` or `config/db_config.py`
- Ensure `etl_warehouse` database exists: `createdb etl_warehouse`

### Missing Data Files
- Ensure `data/raw/bookings.csv` and `data/raw/grounds.xlsx` exist
- Verify file paths in `etl_py/extract.py`

### API Request Failures
- Check internet connection
- Verify JSONPlaceholder API is accessible: `curl https://jsonplaceholder.typicode.com/users`

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure virtual environment is activated

---

## 📈 Data Warehouse Analytics

The star schema enables efficient OLAP queries for:
- **User Analysis** - Booking patterns, preferences, demographics
- **Facility Analysis** - Utilization rates, revenue by ground
- **Temporal Analysis** - Seasonal trends, peak booking times
- **Financial Analysis** - Total revenue, average booking value

---

## 📝 Configuration Files

### `config/db_config.py`
PostgreSQL connection configuration. Uses environment variables:
- `DB_HOST` - Database server
- `DB_PORT` - PostgreSQL port
- `DB_NAME` - Warehouse database name
- `DB_USER` - PostgreSQL user
- `DB_PASSWORD` - PostgreSQL password

### `db/schema.sql`
DDL statements for creating dimension and fact tables. Automatically executed by `load.py`.

### `requirements.txt`
Python package dependencies with versions.

---

## 🎯 Key Features

✅ Multi-source data extraction (CSV, Excel, APIs)  
✅ Dimensional modeling (star schema)  
✅ Data quality & cleaning  
✅ Automated schema creation  
✅ PostgreSQL integration via SQLAlchemy  
✅ Environment-based configuration  
✅ Both Jupyter notebooks and Python modules  
✅ Comprehensive error handling  

---

## 📚 References

- [Kimball Dimensional Modeling](https://www.kimballgroup.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)

---

## 👨‍💼 Assignment Details

**Course:** Data Warehouse and Mining  
**Assignment:** Assignment 1 - ETL Pipeline  
**Semester:** 7th  
**University:** [Your University]  

---

## 📄 License

This project is part of an academic assignment. 

---

## ✉️ Support

For questions or issues, please contact the course instructor or open an issue in the repository.

