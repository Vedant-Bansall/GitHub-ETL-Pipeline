import glob

import duckdb
import pandas as pd
import streamlit as st


# Get the latest parquet file path
def get_latest_parquet_path():
    par_files = glob.glob("data/parquet/*.parquet")
    if not par_files:
        return None
    else:
        return sorted(par_files)[-1]  # noqa: FURB192

# Cache function to load data to Streamlit dashboard
@st.cache_data
def load_data(file_path):
    connection = duckdb.connect(database=':memory:')
    query = f"SELECT * FROM '{file_path}'"
    df = connection.execute(query).df()
    connection.close()
    return df

# Main app execution
def main():
    current_par = get_latest_parquet_path()
    if current_par is None:
        st.warning("No Snapshots Found! Run main.py first!")

    else:
        df = load_data(current_par)
        with st.sidebar:
            selected_authors = st.multiselect("Select Authors", options=df["author"].unique())
            search_term = st.text_input("Search Titles")

        filtered_df = df.copy()

        if selected_authors:
            filtered_df = filtered_df[filtered_df["author"].isin(selected_authors)]

        if search_term:
            filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False, na=False)]

        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()