from pathlib import Path
import pandas as pd
from config.db_config import get_pg_connection, get_sqlalchemy_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "db" / "schema.sql"


def _ensure_schema():
    """Create database schema from schema.sql if it exists"""
    if not SCHEMA_PATH.exists():
        print(f"Schema file not found at {SCHEMA_PATH}, skipping schema creation.")
        return

    sql_text = SCHEMA_PATH.read_text()

    conn = get_pg_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_text)
        conn.commit()
        print("Database schema applied from schema.sql.")
    except Exception as exc:
        print(f"Warning while applying schema.sql (often safe to ignore if tables already exist): {exc}")
        conn.rollback()
    finally:
        conn.close()


def load_data(dim_users, dim_grounds, dim_date, fact_bookings, schema):
    """Load dimension and fact tables to the database"""
    _ensure_schema()
    engine = get_sqlalchemy_engine()

    def to_sql(df, name):
        print(f"Loading {name} with {len(df)} rows ...")
        df.to_sql(name, engine, if_exists="append", index=False, schema=schema)

    to_sql(dim_users, "dim_users")
    to_sql(dim_grounds, "dim_grounds")
    to_sql(dim_date, "dim_date")
    to_sql(fact_bookings, "fact_bookings")

    print("All tables loaded successfully.")
