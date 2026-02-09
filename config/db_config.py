import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "etl_warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


# Psycopg2 Connection (for raw SQL)


def get_pg_connection():
    # Create and return PostgreSQL connection using psycopg2
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("PostgreSQL connection successful")
        return conn

    except Exception as e:
        print("Database connection failed:", e)
        raise



# SQLAlchemy Engine (for pandas to_sql)
def get_sqlalchemy_engine():
    # Create SQLAlchemy engine for pandas loading
    try:
        url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(url)
        print("SQLAlchemy engine created")
        return engine

    except Exception as e:
        print(" Engine creation failed:", e)
        raise


# Test Runner
if __name__ == "__main__":
    conn = get_pg_connection()
    conn.close()

    engine = get_sqlalchemy_engine()

#