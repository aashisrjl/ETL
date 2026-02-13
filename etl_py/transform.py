import numpy as np
import pandas as pd


def build_dim_users(df_users):
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


def build_dim_grounds(df_grounds):

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


def build_dim_date(df_bookings):

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


def build_fact_bookings(df_bookings, dim_date):
 
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


def fill_numeric(df):
    """Fill numerical missing data with median"""
    num_cols = df.select_dtypes(include=np.number).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
    return df


def fill_categorical(df):
    """Fill categorical missing data with mode"""
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown')
    return df


def remove_duplicates(df):
    """Remove duplicate rows"""
    df = df.drop_duplicates()
    return df


def remove_index(df):
    """Reset index"""
    df = df.reset_index(drop=True)
    return df


def standarize_names(df):
    """Standardize column names to lowercase with underscores"""
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def fix_date_format(df):
    """Convert date columns to datetime format"""
    date_mask = df.columns.str.contains('date|Date|DATE', case=False, na=False)
    date_columns = df.columns[date_mask]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def detect_remove_outliers(df):
    """Detect and remove outliers using IQR method"""
    num_cols = df.select_dtypes(include=np.number).columns
    for col in num_cols:
        Q1 = df[col].quantile(0.20)
        Q3 = df[col].quantile(0.80)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        print(f"Outliers in {col}: {len(outliers)}")
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df


def noise_reduction(df):
    """Reduce noise in data"""
    return df


def clean_grounds(df_grounds):
    """Clean grounds data"""
    df_grounds = fill_numeric(df_grounds)
    df_grounds = fill_categorical(df_grounds)
    df_grounds = remove_duplicates(df_grounds)
    df_grounds = standarize_names(df_grounds)
    df_grounds = remove_index(df_grounds)
    df_grounds = fix_date_format(df_grounds)
    return df_grounds


def clean_bookings(df_bookings):
    """Clean bookings data"""
    df_bookings = fill_numeric(df_bookings)
    df_bookings = fill_categorical(df_bookings)
    df_bookings = remove_duplicates(df_bookings)
    df_bookings = standarize_names(df_bookings)
    df_bookings = remove_index(df_bookings)
    df_bookings = fix_date_format(df_bookings)
    return df_bookings


def clean_users(df_users):
    """Clean users data"""
    df_users = fill_numeric(df_users)
    df_users = fill_categorical(df_users)
    df_users = remove_duplicates(df_users)
    df_users = standarize_names(df_users)
    df_users = remove_index(df_users)
    df_users = fix_date_format(df_users)
    return df_users


def transform_data(df_bookings, df_grounds, df_users):
    """Transform raw data into dimensional and fact tables"""
    
    # Clean bookings
    df_bookings = df_bookings.copy()
    df_bookings = clean_bookings(df_bookings)

    df_grounds = df_grounds.copy()
    df_grounds = clean_grounds(df_grounds)

    df_users = df_users.copy()
    df_users = clean_users(df_users)

    # Build dimensions table
    dim_users = build_dim_users(df_users)
    dim_grounds = build_dim_grounds(df_grounds)
    dim_date = build_dim_date(df_bookings)

    # Build fact table
    fact_bookings = build_fact_bookings(df_bookings, dim_date)

    return dim_users, dim_grounds, dim_date, fact_bookings
