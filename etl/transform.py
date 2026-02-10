
    # * dim_users
    # * dim_grounds
    # * dim_date


from typing import Tuple

import numpy as np
import pandas as pd


def _build_dim_users(df_users: pd.DataFrame) -> pd.DataFrame:
    df = df_users.copy()

    # Align IDs with bookings (201.. instead of 1..)
    df["user_id"] = df["id"] + 200

    dim_users = pd.DataFrame(
        {
            "user_id": df["user_id"],
            "name": df.get("name"),
            "username": df.get("username"),
            "email": df.get("email"),
            "phone": df.get("phone"),
            "website": df.get("website"),
            "city": df.get("address.city"),
            "company": df.get("company.name"),
        }
    )

    # Drop potential duplicates on user_id to be safe
    dim_users = dim_users.drop_duplicates(subset=["user_id"])

    return dim_users


def _build_dim_grounds(df_grounds: pd.DataFrame) -> pd.DataFrame:

    df = df_grounds.copy()

    dim_grounds = pd.DataFrame(
        {
            "ground_id": df["ground_id"],
            "ground_name": df["ground_name"],
            "location": df["city"],
            "ground_type": df["location_type"],
            "price_per_hour": df["price_per_hour"],
            "is_active": True,
        }
    )

    dim_grounds = dim_grounds.drop_duplicates(subset=["ground_id"])

    return dim_grounds


def _build_dim_date(df_bookings: pd.DataFrame) -> pd.DataFrame:

    dates = pd.to_datetime(df_bookings["booking_date"], errors="coerce").dropna().drop_duplicates()
    dates = dates.sort_values()

    dim_date = pd.DataFrame({"full_date": dates})

    dim_date["date_id"] = range(1, len(dim_date) + 1)
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["weekday"] = dim_date["full_date"].dt.weekday + 1  # 1=Monday
    dim_date["weekday_name"] = dim_date["full_date"].dt.day_name()

    # Reorder columns to match schema more closely
    dim_date = dim_date[
        [
            "date_id",
            "full_date",
            "day",
            "month",
            "year",
            "quarter",
            "weekday",
            "weekday_name",
        ]
    ]

    return dim_date


def _build_fact_bookings(
    df_bookings: pd.DataFrame,
    dim_date: pd.DataFrame,
) -> pd.DataFrame:
 
    df = df_bookings.copy()

    # Ensure booking_date is datetime for joining
    df["booking_date"] = pd.to_datetime(df["booking_date"], errors="coerce")

    # Join to get date_id from dim_date
    df = df.merge(dim_date[["date_id", "full_date"]], left_on="booking_date", right_on="full_date", how="left")

    fact_bookings = pd.DataFrame(
        {
            "booking_id": df["booking_id"],
            "user_id": df["user_id"],
            "ground_id": df["ground_id"],
            "date_id": df["date_id"],
            "booking_date": df["booking_date"].dt.date,
            "slot_time": "Unknown",
            "duration_hours": df["hours"],
            "total_price": df["total_price"],
            "booking_status": "Completed",
        }
    )

    return fact_bookings


def transform_data(
    df_bookings: pd.DataFrame,
    df_grounds: pd.DataFrame,
    df_users: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    bookings = df_bookings.copy()

    # ---- Clean bookings ----
    # Fill numeric NaNs with median
    num_cols = bookings.select_dtypes(include=np.number).columns
    for col in num_cols:
        bookings[col] = bookings[col].fillna(bookings[col].median())

    # Fill categorical NaNs with mode
    cat_cols = bookings.select_dtypes(include="object").columns
    for col in cat_cols:
        mode_series = bookings[col].mode()
        if not mode_series.empty:
            bookings[col] = bookings[col].fillna(mode_series[0])

    # Ensure booking_date is datetime
    bookings["booking_date"] = pd.to_datetime(bookings["booking_date"], errors="coerce")

    # ---- Build dimensions ----
    dim_users = _build_dim_users(df_users)
    dim_grounds = _build_dim_grounds(df_grounds)
    dim_date = _build_dim_date(bookings)

    # ---- Build fact table ----
    fact_bookings = _build_fact_bookings(bookings, dim_date)

    return dim_users, dim_grounds, dim_date, fact_bookings


if __name__ == "__main__":
    # This block can be used for quick manual testing in a REPL/notebook.
    from etl.extract import extract_data

    b, g, u = extract_data()
    d_users, d_grounds, d_date, f_bookings = transform_data(b, g, u)
    print("dim_users:", d_users.shape)
    print("dim_grounds:", d_grounds.shape)
    print("dim_date:", d_date.shape)
    print("fact_bookings:", f_bookings.shape)

