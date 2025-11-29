import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -------------------------
# 🔹 DATA LOADING
# -------------------------
@st.cache_data(show_spinner=False)
def load_data_versions():
    """Load current and previous processed files."""
    try:
        current = pd.read_csv("data/processed_files_for_DQ/processed_v2.csv")
        previous = pd.read_csv("data/processed_files_for_DQ/processed_v1.csv")
        return current, previous
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()


# -------------------------
# 🔹 COMPLETENESS CHECK
# -------------------------
def check_completeness(df):
    completeness = df.isnull().sum().reset_index()
    completeness.columns = ['Column', 'Missing Values']
    completeness['% Missing'] = (completeness['Missing Values'] / len(df)) * 100
    return completeness


def plot_completeness_chart(completeness_df):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=completeness_df.sort_values('% Missing', ascending=False),
        x='% Missing', y='Column', palette='Blues_r', ax=ax
    )
    ax.set_title("Missing Values (%) by Column")
    ax.set_xlabel("Percentage Missing")
    ax.set_ylabel("Columns")
    plt.tight_layout()
    return fig


# -------------------------
# 🔹 UNIQUENESS CHECK
# -------------------------
def check_uniqueness(df):
    unique_counts = df.nunique().reset_index()
    unique_counts.columns = ['Column', 'Unique Count']
    unique_counts['% Unique'] = (unique_counts['Unique Count'] / len(df)) * 100
    return unique_counts


def plot_uniqueness_chart(unique_df):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=unique_df.sort_values('% Unique', ascending=False),
        x='% Unique', y='Column', palette='Greens', ax=ax
    )
    ax.set_title("Unique Values (%) by Column")
    ax.set_xlabel("Percentage Unique")
    ax.set_ylabel("Columns")
    plt.tight_layout()
    return fig


# -------------------------
# 🔹 DUPLICATE CHECKS
# -------------------------
def check_duplicates(df):
    """Find completely duplicate rows."""
    return df[df.duplicated()]


def check_date_duplicates(df, date_column="date"):
    """Check for duplicate entries based on a given date column."""
    if date_column not in df.columns:
        return pd.DataFrame(), f"⚠️ Column '{date_column}' not found in dataset."

    duplicates = df[df.duplicated(subset=[date_column], keep=False)]
    if duplicates.empty:
        return pd.DataFrame(), "✅ No duplicate records found for date column."
    else:
        return duplicates, f"❌ Found {len(duplicates)} duplicate records based on '{date_column}'."


# -------------------------
# 🔹 VERSION COMPARISON
# -------------------------
def compare_versions(current, previous):
    """Compare old vs new file for added/removed/changed rows."""
    comparison = {}
    try:
        added = pd.concat([current, previous, previous]).drop_duplicates(keep=False)
        removed = pd.concat([previous, current, current]).drop_duplicates(keep=False)
    except Exception:
        added, removed = pd.DataFrame(), pd.DataFrame()

    comparison["Added Rows"] = added
    comparison["Removed Rows"] = removed
    return comparison


# -------------------------
# 🔹 MAIN WRAPPER
# -------------------------
def run_data_quality():
    """Run all data quality checks together."""
    current, previous = load_data_versions()

    if current.empty:
        st.error("No current data loaded.")
        return {}

    completeness_df = check_completeness(current)
    uniqueness_df = check_uniqueness(current)
    duplicates_df = check_duplicates(current)
    date_dupes, date_msg = check_date_duplicates(current, date_column="date")
    comparison = compare_versions(current, previous)

    # Build visualizations
    completeness_fig = plot_completeness_chart(completeness_df)
    uniqueness_fig = plot_uniqueness_chart(uniqueness_df)

    results = {
        "completeness": completeness_df,
        "uniqueness": uniqueness_df,
        "duplicates": duplicates_df,
        "date_duplicates": date_dupes,
        "date_message": date_msg,
        "comparison": comparison,
        "completeness_fig": completeness_fig,
        "uniqueness_fig": uniqueness_fig
    }

    return results
