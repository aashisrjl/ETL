from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data


def run_etl():

    # 1. Extract
    df_bookings, df_grounds, df_users = extract_data()

    # 2. Transform
    dim_users, dim_grounds, dim_date, fact_bookings = transform_data(
        df_bookings, df_grounds, df_users
    )

    # 3. Load
    load_data(dim_users, dim_grounds, dim_date, fact_bookings)


if __name__ == "__main__":
    run_etl()

