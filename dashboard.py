import glob
from collections import Counter

import duckdb
import pandas as pd
import plotly.express as px
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
    query = f"SELECT *, '{file_path}' as filename FROM '{file_path}'"
    df = connection.execute(query).df()
    connection.close()
    
    # Extract snapshot_time
    df["snapshot_time"] = df["filename"].str.extract(r'(\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2})') # Regex Timestamp
    df["snapshot_time"] = pd.to_datetime(df["snapshot_time"], format="%Y-%m-%d_%H.%M.%S") # Convert to Datetime
    return df # Return DF

# Get all records of parquet files
@st.cache_data
def get_all_records():
    df = duckdb.sql("SELECT *, filename FROM read_parquet('data/parquet/*.parquet', filename=True, union_by_name=True)").df() # Create DF of all parquet records
    df["snapshot_time"] = df["filename"].str.extract(r'(\d{4}-\d{2}-\d{2}_\d{2}\.\d{2}\.\d{2})') # Regex Timestamp and create column
    df["snapshot_time"] = pd.to_datetime(df["snapshot_time"], format="%Y-%m-%d_%H.%M.%S") # Create Datetime object
    return df # Return DF

# Main app execution
def main():
    current_par = get_latest_parquet_path()
    # If no data found, do not run
    if current_par is None:
        st.warning("No Snapshots Found! Run main.py first!")

    # Run main app
    else:
        # DataFrames
        df = load_data(current_par) # Get Latest Snapshot DataFrame
        df_all = get_all_records() # Get DF of all time

        # Set to wide width
        st.set_page_config(page_title="GitHub ETL Dashboard", layout="wide")

        # Sidebar creation
        with st.sidebar:
            selected_authors = st.multiselect("Select Authors", options=df["author"].unique()) # Select authors
            selected_entity = st.multiselect("Select Entity Type", default=df_all["entity_type"].unique(), options=df_all["entity_type"].unique()) # Select Entity Type
            search_term = st.text_input("Search Titles") # Search for title
            # Search by time
            df_all["snapshot_time"] = pd.to_datetime(df_all["snapshot_time"]) # Convert to datetime
            min_date = df_all["snapshot_time"].min().date()
            max_date = df_all["snapshot_time"].max().date()
            selected_dates = st.sidebar.date_input("Filter via date", value=(min_date, max_date), min_value=min_date, max_value=max_date) # Create the date input

        # Filtering selected authors/topics
        filtered_df = df.copy()

        # Filtering authors
        if selected_authors:
            filtered_df = filtered_df[filtered_df["author"].isin(selected_authors)]

        # Filtering selected topics
        if search_term:
            filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False, na=False)]

        # Filtering issues/PRs
        if selected_entity:
            filtered_df = filtered_df[filtered_df["entity_type"].isin(selected_entity)]

        # Filters dates
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates
            filtered_df = filtered_df[filtered_df["snapshot_time"].dt.date.between(start_date, end_date)]

        elif len(selected_dates) == 1:
            filtered_df = filtered_df[filtered_df["snapshot_time"].dt.date == selected_dates[0]]

        # Creating KPI Cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Issues Recorded", len(filtered_df)) # Total Issues Recorded Card

        with col2:
            st.metric("Unique authors", filtered_df["author"].nunique()) # Unique Authors Column

        with col3:
            st.metric("Amount of stale items", filtered_df["is_stale"].sum()) # Amount of stale items column

        # Seperate cards from Graphs
        st.divider()

        # Creating Grids for First 2 Graphs
        grid_col1, grid_col2 = st.columns(2)

        # First grid column
        with grid_col1.container(border=True):
            # Open to closed ratio pie chart
            states = filtered_df["state"].value_counts()
            fig = px.pie(values=states.values, names=states.index, title="Amount of open/closed issues")
            st.plotly_chart(fig, use_container_width=True)

        # Second grid column
        with grid_col2.container(border=True):
            # Authors and how many issues they have made
            st.subheader("Amount of issues an author made")
            st.bar_chart(filtered_df["author"].value_counts(), x_label="Author", y_label="Amount of issues recorded")

        # Other 2 graphs
        with st.container(border=True):
            # Labels Bar chart and how many there are of each
            all_labels = []
            for label_list in filtered_df["labels"]:
                for label in label_list:
                    all_labels.append(label)  # noqa: PERF402
            cnt = Counter(all_labels)
            labels_df = pd.DataFrame.from_dict(cnt, orient="index")
            st.subheader("Amount of labels recorded")
            st.bar_chart(labels_df, x_label="Labels", y_label="Amounts")

            # Histogram of lead time days to see how long it takes to close an issue
            histogram_fig = px.histogram(
                filtered_df["lead_time_days"].dropna(),
                x="lead_time_days",
                text_auto=True,
                labels={
                    "lead_time_days": "Lead Time (Days)",
                    "count": "Total Items"
                },
                title="Lead Time Distribution")
            st.plotly_chart(histogram_fig, use_container_width=True)

        # Total Issue/PR over time
        if selected_entity:
            filtered_df_all = df_all[df_all["entity_type"].isin(selected_entity)]

            # Filters dates
            if len(selected_dates) == 2:
                start_date, end_date = selected_dates
                filtered_df_all = filtered_df_all[filtered_df_all["snapshot_time"].dt.date.between(start_date, end_date)]

            elif len(selected_dates) == 1:
                filtered_df_all = filtered_df_all[filtered_df_all["snapshot_time"].dt.date == selected_dates[0]]

            trend_df = filtered_df_all.groupby(["snapshot_time", "entity_type"]).size().reset_index(name="count")

            fig_trend = px.line(trend_df,
                                x="snapshot_time",
                                y="count",
                                color="entity_type",
                                markers=True,
                                title="Issues and PRs Over Time")
            st.plotly_chart(fig_trend, use_container_width=True)

        else:
            st.warning("Please select at least one entity type")

        # View raw data
        with st.expander("View Raw Data"):
            st.dataframe(filtered_df) # See the raw Streamlit dataframe

# Run the actual dashboard
if __name__ == "__main__":
    main()