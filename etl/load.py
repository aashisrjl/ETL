"""
Load step for the ETL pipeline.

Responsible for:
- creating tables in PostgreSQL using db/schema.sql
- loading dimension and fact tables using pandas.to_sql
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from config.db_config import get_pg_connection, get_sqlalchemy_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "db" / "schema.sql"


def _ensure_schema():
    """
    Execute the schema.sql file to create tables if they don't exist.

    If tables already exist, PostgreSQL will raise an error on CREATE TABLE.
    We simply print a warning in that case and continue.
    """
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
        # Common case: tables already exist
        print(f"Warning while applying schema.sql (often safe to ignore if tables already exist): {exc}")
        conn.rollback()
    finally:
        conn.close()


def load_data(
    dim_users: pd.DataFrame,
    dim_grounds: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_bookings: pd.DataFrame,
    schema: Optional[str] = None,
):
    """
    Load dimension and fact tables into PostgreSQL.

    Parameters
    ----------
    dim_users, dim_grounds, dim_date, fact_bookings : DataFrame
        Transformed tables ready to be loaded.
    schema : str, optional
        Optional PostgreSQL schema name. If provided, tables will be created
        under this schema.
    """
    # Make sure the tables exist
    _ensure_schema()

    engine = get_sqlalchemy_engine()

    def _to_sql(df: pd.DataFrame, name: str):
        print(f"Loading {name} with {len(df)} rows ...")
        df.to_sql(name, engine, if_exists="append", index=False, schema=schema)

    _to_sql(dim_users, "dim_users")
    _to_sql(dim_grounds, "dim_grounds")
    _to_sql(dim_date, "dim_date")
    _to_sql(fact_bookings, "fact_bookings")

    print("All tables loaded successfully.")


if __name__ == "__main__":
    # Simple end-to-end manual test (will try to hit your DB).
    from etl.extract import extract_data
    from etl.transform import transform_data

    b, g, u = extract_data()
    d_users, d_grounds, d_date, f_bookings = transform_data(b, g, u)
    load_data(d_users, d_grounds, d_date, f_bookings)

