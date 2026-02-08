import requests
import pandas as pd
import os
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")

def fetch_users():
    r = requests.get(EXTERNAL_API_URL)
    data = r.json()

    df = pd.json_normalize(data)

    # pick useful columns
    df = df[[
        "id",
        "name",
        "email",
        "address.city",
        "company.name",
        "phone"
    ]]

    df.columns = [
        "user_id",
        "name",
        "email",
        "city",
        "company",
        "phone"
    ]

    return df
