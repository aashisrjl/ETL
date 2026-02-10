import requests
import pandas as pd
# from config.db_config import get_pg_connection, get_sqlalchemy_engine

# conn = get_pg_connection()
# engine = get_sqlalchemy_engine()

#csv
df_bookings=pd.read_csv("../data/raw/bookings.csv")

#xlsx
df_grounds=pd.read_excel("../data/raw/grounds.xlsx")

# api
url = "https://jsonplaceholder.typicode.com/users"
df_users = pd.json_normalize(users)
users = requests.get(url).json()


