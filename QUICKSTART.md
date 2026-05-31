# 🚀 Quick Start Guide - How to Run the ETL Project

This guide walks you through setting up and running the ETL pipeline step-by-step.

---

## 📋 Prerequisites

Before running the project, ensure you have:

- **Python 3.8+** installed
- **PostgreSQL 12+** installed and running
- **Git** (for cloning)
- **Basic command line knowledge**

### Check Prerequisites

```bash
# Check Python version
python3 --version

# Check PostgreSQL version
psql --version

# Check PostgreSQL service status
pg_isready
```

---

## ⚙️ Step 1: Clone Repository & Navigate to Project

```bash
# Clone the repository (or extract if downloaded)
git clone <repository-url>
cd Assignment1-ETL

# Or if already in the directory:
cd /home/aashis-rijal/Downloads/7th_sem/Data_warehouse_and_mining/Assignments/Assignment1-ETL
```

---

## 🔧 Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv etlenv

# Activate virtual environment
source etlenv/bin/activate

# On Windows, use:
# etlenv\Scripts\activate
```

**Verify activation:**
```bash
# You should see (etlenv) in your terminal prompt
which python  # Should show path to etlenv/bin/python
```

---

## 📦 Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list | grep -E 'pandas|psycopg2|SQLAlchemy|requests'
```

---

## 🗄️ Step 4: Setup PostgreSQL Database

### 4A: Create Database

```bash
# Create the ETL warehouse database
createdb etl_warehouse

# Verify creation
psql -l | grep etl_warehouse
```

**On Windows (using psql):**
```bash
psql -U postgres -c "CREATE DATABASE etl_warehouse;"
```

### 4B: Configure Database Credentials

Create a `.env` file in the project root:

```bash
# Create .env file
nano .env
```

**Add these contents:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_warehouse
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

Replace `your_postgres_password` with your actual PostgreSQL password.

**Verify .env file:**
```bash
cat .env  # Should show your credentials
```

---

## ✅ Step 5: Verify Data Files

Ensure all input data files exist:

```bash
# Check for required data files
ls -la data/raw/

# Expected output:
# bookings.csv      (Booking data)
# grounds.xlsx      (Sports grounds data)
# users_api.json    (API response cache - optional)
```

If files are missing:
- `bookings.csv` - Ensure this file exists in `data/raw/`
- `grounds.xlsx` - Ensure this file exists in `data/raw/`

---

## 🎯 Step 6: Run the ETL Pipeline

### **Option A: Run Using Python (Recommended for Production)**

```bash
# Make sure virtual environment is activated
source etlenv/bin/activate

# Run the main ETL script
python main.py
```

**Expected Output:**
```
Extracting data from all sources...
PostgreSQL connection successful
Data extracted successfully
Transforming data...
Building dim_users... (10 rows)
Building dim_grounds... (5 rows)
Building dim_date... (365 rows)
Building fact_bookings... (100 rows)
Loading to PostgreSQL...
Database schema applied from schema.sql
Loading dim_users with 10 rows...
Loading dim_grounds with 5 rows...
Loading dim_date with 365 rows...
Loading fact_bookings with 100 rows...
All tables loaded successfully!
ETL Pipeline Complete! ✅
```

### **Option B: Run Using Jupyter Notebooks (Interactive)**

```bash
# Activate virtual environment
source etlenv/bin/activate

# Start Jupyter
jupyter notebook
```

This opens a browser window. Navigate to:
1. **main.ipynb** - Main orchestration notebook
   - Or individual notebooks:
   - **etl/extract.ipynb** - Data extraction
   - **etl/transform.ipynb** - Data transformation
   - **etl/load.ipynb** - Data loading

**How to run Jupyter cells:**
- Click on a cell
- Press `Shift + Enter` to run it
- Or click the ▶ Run button

---

## 🔍 Step 7: Verify ETL Success

### 7A: Check Database Connection

```bash
# Connect to PostgreSQL
psql -U postgres -d etl_warehouse

# Inside psql, check tables
\dt

# Expected output:
# dim_users | table | postgres
# dim_grounds | table | postgres
# dim_date | table | postgres
# fact_bookings | table | postgres
```

### 7B: Verify Data Loaded

```sql
-- Inside psql terminal
-- Check record counts
SELECT 'dim_users' as table_name, COUNT(*) as records FROM dim_users
UNION ALL
SELECT 'dim_grounds', COUNT(*) FROM dim_grounds
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'fact_bookings', COUNT(*) FROM fact_bookings;

-- Expected Output:
--     table_name   | records
-- ---------------+---------
--  dim_users      |      10
--  dim_grounds    |       5
--  dim_date       |     365
--  fact_bookings  |     100
```

### 7C: Sample Query

```sql
-- View sample booking data with details
SELECT 
    f.booking_id,
    u.name as user_name,
    g.ground_name,
    f.booking_date,
    f.total_price,
    f.booking_status
FROM fact_bookings f
JOIN dim_users u ON f.user_id = u.user_id
JOIN dim_grounds g ON f.ground_id = g.ground_id
LIMIT 5;

-- Exit psql
\q
```

---

## 📊 Step 8: Run Sample Queries

### Query 1: Total Revenue by Ground
```bash
psql -U postgres -d etl_warehouse -c "
SELECT 
    g.ground_name,
    SUM(f.total_price) as total_revenue,
    COUNT(f.booking_id) as bookings
FROM fact_bookings f
JOIN dim_grounds g ON f.ground_id = g.ground_id
WHERE f.booking_status = 'confirmed'
GROUP BY g.ground_name
ORDER BY total_revenue DESC;
"
```

### Query 2: Top Users by Bookings
```bash
psql -U postgres -d etl_warehouse -c "
SELECT 
    u.name,
    COUNT(f.booking_id) as total_bookings,
    SUM(f.total_price) as total_spent
FROM fact_bookings f
JOIN dim_users u ON f.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY total_bookings DESC LIMIT 5;
"
```

---

## 🔄 Step 9: Re-run ETL Pipeline (Update Data)

If you need to reload data or make changes:

### Option 1: Full Reload (Recommended)

```bash
# 1. Delete existing tables (WARNING: This deletes data!)
psql -U postgres -d etl_warehouse -c "
DROP TABLE IF EXISTS fact_bookings CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_grounds CASCADE;
DROP TABLE IF EXISTS dim_users CASCADE;
"

# 2. Re-run ETL
python main.py
```

### Option 2: Keep Existing Data & Append

```bash
# Simply run the ETL again - it will append new data
python main.py
```

---

## 🐛 Troubleshooting

### Issue 1: "psycopg2.OperationalError: could not connect to server"

**Cause:** PostgreSQL not running or credentials wrong

**Solution:**
```bash
# Check PostgreSQL status
sudo service postgresql status

# Start PostgreSQL (if stopped)
sudo service postgresql start

# Verify connection
psql -U postgres -d etl_warehouse

# Check .env file credentials are correct
cat .env
```

### Issue 2: "ModuleNotFoundError: No module named 'pandas'"

**Cause:** Dependencies not installed or virtual environment not activated

**Solution:**
```bash
# Verify virtual environment is activated (should see (etlenv) in prompt)
source etlenv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep pandas
```

### Issue 3: "FileNotFoundError: data/raw/bookings.csv"

**Cause:** Data files missing or in wrong location

**Solution:**
```bash
# Check if files exist
ls -la data/raw/

# Ensure you're in the correct project directory
pwd  # Should end with Assignment1-ETL

# Create missing files or verify paths in extract.py
```

### Issue 4: "Could not locate a column in row for column 'xxx'"

**Cause:** Excel file missing columns or CSV has wrong format

**Solution:**
```bash
# Verify Excel file structure
python3 -c "
import pandas as pd
df = pd.read_excel('data/raw/grounds.xlsx')
print(df.head())
print(df.columns)
"

# Verify CSV file structure
python3 -c "
import pandas as pd
df = pd.read_csv('data/raw/bookings.csv')
print(df.head())
print(df.columns)
"
```

### Issue 5: "Connection refused" when running ETL

**Cause:** Cannot connect to PostgreSQL

**Solution:**
```bash
# Test PostgreSQL connection
pg_isready -h localhost -p 5432

# If not running, start it:
sudo systemctl start postgresql

# Or on Mac:
brew services start postgresql
```

---

## 📈 Next Steps After Successful Run

### 1. Explore the Data

```bash
# Connect to database
psql -U postgres -d etl_warehouse

# List all tables
\dt

# View table schemas
\d dim_users
\d fact_bookings

# Run custom queries
SELECT * FROM dim_users LIMIT 5;
```

### 2. Create Analysis Queries

```bash
# Monthly revenue trends
SELECT 
    d.year, 
    d.month, 
    SUM(f.total_price) as monthly_revenue
FROM fact_bookings f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

### 3. Modify Data Files

- Edit `data/raw/bookings.csv` - Add new bookings
- Edit `data/raw/grounds.xlsx` - Add new facilities
- Re-run ETL pipeline to update warehouse

### 4. Extend the Pipeline

- Add new data sources in `etl_py/extract.py`
- Create new dimensions in `etl_py/transform.py`
- Update schema in `db/schema.sql`
- Re-run pipeline

---

## 🎓 Learning Resources

### Understanding the Code

1. **Extract Phase** - See [`etl_py/extract.py`](etl_py/extract.py)
   - How data is read from CSV, Excel, and API

2. **Transform Phase** - See [`etl_py/transform.py`](etl_py/transform.py)
   - How data is cleaned and modeled

3. **Load Phase** - See [`etl_py/load.py`](etl_py/load.py)
   - How data is inserted into PostgreSQL

4. **Database Schema** - See [`db/schema.sql`](db/schema.sql)
   - Table definitions and relationships

### Useful Commands

```bash
# View current working directory
pwd

# List project files
ls -la

# View file contents
cat filename.txt

# Run Python script directly
python3 script.py

# Exit PostgreSQL
\q

# List PostgreSQL databases
psql -l

# Drop a database
dropdb etl_warehouse

# Check Python packages
pip list
```

---

## ✨ Quick Reference Commands

| Task | Command |
|------|---------|
| Activate env | `source etlenv/bin/activate` |
| Deactivate env | `deactivate` |
| Install packages | `pip install -r requirements.txt` |
| Create DB | `createdb etl_warehouse` |
| Drop DB | `dropdb etl_warehouse` |
| Run ETL | `python main.py` |
| Run Jupyter | `jupyter notebook` |
| Connect to DB | `psql -U postgres -d etl_warehouse` |
| Check tables | `\dt` (in psql) |
| Run query | `SELECT * FROM dim_users;` (in psql) |
| Exit psql | `\q` |

---

## 🎯 Summary

**Minimal 5-Step Setup:**
```bash
1. cd Assignment1-ETL
2. source etlenv/bin/activate
3. pip install -r requirements.txt
4. createdb etl_warehouse
5. python main.py
```

**Expected Result:**
- ✅ Database created
- ✅ 4 tables created (3 dimensions + 1 fact)
- ✅ 100+ records loaded
- ✅ Ready for analysis

---

## 📞 Need Help?

- Check [REPORT.md](REPORT.md) - Comprehensive technical documentation
- Check [README.md](README.md) - Project overview
- Review error messages carefully
- Verify database connectivity with `pg_isready`
- Check all data files exist in `data/raw/`

---

**Happy analyzing! 🎉**
