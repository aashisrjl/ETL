import requests
import pandas as pd


def extract_data():

    # CSV
    df_bookings = pd.read_csv("../data/raw/bookings.csv")

    # Excel
    df_grounds = pd.read_excel("../data/raw/grounds.xlsx")

    # API
    url = "https://jsonplaceholder.typicode.com/users"
    users = requests.get(url).json()
    df_users = pd.json_normalize(users)

    return df_bookings, df_grounds, df_users


if __name__ == "__main__":
    # Simple manual test: run this file directly to preview shapes
    b, g, u = extract_data()
    print("Bookings:", b.shape)
    print("Grounds:", g.shape)
    print("Users:", u.shape)
