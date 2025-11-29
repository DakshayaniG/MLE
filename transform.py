def transform(dataframe):
    # example transformation
    df = dataframe.copy()
    df["name_upper"] = df["name"].str.upper()
    df["age_group"] = df["age"].apply(lambda x: "young" if x < 35 else "senior")
    df["salary_in_k"] = df["salary"] / 1000
    return df
