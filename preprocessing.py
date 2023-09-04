import os

import pandas as pd

top200_path = os.path.join(".", "top200.csv")
top200 = pd.read_csv(top200_path)
names = top200["name"].tolist()

for name in names:
    input_file_path = os.path.join(".", "csvs", f"{name}_9_2_2022-9_2_2023_historical_data_coinmarketcap.csv")
    df = pd.read_csv(
        input_file_path,
        sep=";",
    )

    df["timehigh"] = pd.to_datetime(df["timeHigh"]).dt.time
    df["timelow"] = pd.to_datetime(df["timeLow"]).dt.time
    df["date"] = pd.to_datetime(
        df["timestamp"]).dt.date.astype("datetime64[s]")

    df.drop(
        columns=["timeOpen", "timeClose", "timeHigh", "timeLow", "timestamp"],
        inplace=True,
    )
    df = df[
        [
            "date",
            "timelow",
            "low",
            "timehigh",
            "high",
            "open",
            "close",
            "volume",
            "marketCap",
        ]
    ]
    output_file_path = os.path.join(".", "cleaned_csvs", f"{name}.csv")
    df.to_csv(
        output_file_path,
        index=False,
    )
