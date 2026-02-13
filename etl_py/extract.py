import requests
import pandas as pd
from pathlib import Path


def users_data():
    url = "https://jsonplaceholder.typicode.com/users"
    users = requests.get(url).json()
    df_users = pd.json_normalize(users)
    return df_users


def extract_data():
    # Get the project root directory (parent of etl_py)
    project_root = Path(__file__).resolve().parent.parent
    
    # CSV
    df_bookings = pd.read_csv(project_root / "data" / "raw" / "bookings.csv")

    # Excel
    df_grounds = pd.read_excel(project_root / "data" / "raw" / "grounds.xlsx")

    # API
    df_users = users_data()

    return df_bookings, df_grounds, df_users
