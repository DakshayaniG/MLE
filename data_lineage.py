import pandas as pd
import json
import os
import importlib.util
import streamlit as st

# ✅ Cache only serializable data
@st.cache_data(show_spinner=False)
def load_serializable_data():
    """Load only data & config (cacheable)."""
    base_path = os.path.join(os.getcwd(), "data")
    csv_path = os.path.join(base_path, "source.csv")
    config_path = os.path.join(base_path, "config.json")

    df_source = pd.read_csv(csv_path)

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        target_columns = config.get("columns", {})
    else:
        target_columns = {}

    return df_source, target_columns


def load_transform_module():
    """Load the transformation module (not cached, not serializable)."""
    base_path = os.path.join(os.getcwd(), "data")
    transform_path = os.path.join(base_path, "transform.py")
    spec = importlib.util.spec_from_file_location("transform", transform_path)
    transform_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transform_module)
    return transform_module


@st.cache_data(show_spinner=False)
def analyze_lineage():
    """Analyze lineage with optional targets."""
    df_source, target_columns = load_serializable_data()
    transform_module = load_transform_module()

    df_transformed = transform_module.transform(df_source)

    tree = {}
    for s_col in df_source.columns:
        tree[s_col] = {}
        for t_col in df_transformed.columns:
            if s_col in t_col:
                mapped_target = [
                    target_columns[t_col_key]
                    for t_col_key in target_columns.keys()
                    if t_col_key == t_col
                ]
                if mapped_target:
                    tree[s_col][t_col] = mapped_target
                else:
                    tree[s_col][t_col] = ["(🟡 Unmapped column)"]
    return tree
