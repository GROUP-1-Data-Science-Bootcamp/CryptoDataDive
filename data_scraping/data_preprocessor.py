import os

import pandas as pd
top200_path = os.path.join(".", "data_collections/top200.csv")
top200 = pd.read_csv(top200_path)
names = top200["name"].tolist()

for name in names:
    input_file_path = os.path.join(".", "data_collections/csvs", f"{name}_11_09_2022-11_09_2023_historical_data_coinmarketcap.csv")
    df = pd.read_csv(
        input_file_path,
        sep=";",
    )

    df["time_high"] = pd.to_datetime(df["timeHigh"]).dt.time
    df["time_low"] = pd.to_datetime(df["timeLow"]).dt.time
    df["date"] = pd.to_datetime(
        df["timestamp"]).dt.date.astype("datetime64[s]")
    df["market_cap"] = df['marketCap']

    df.drop(
        columns=["timeOpen", "timeClose", "timeHigh", "timeLow", "timestamp"],
        inplace=True,
    )
    df = df[
        [
            "date",
            "time_low",
            "low",
            "time_high",
            "high",
            "open",
            "close",
            "volume",
            "market_cap",
        ]
    ]
    output_file_path = os.path.join(".", "data_collections/cleaned_csvs", f"{name}.csv")
    df.to_csv(
        output_file_path,
        index=False,
    )
