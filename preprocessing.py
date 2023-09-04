import pandas as pd

top200 = pd.read_csv("top200.csv")
names = top200["name"].tolist()

for name in names:
    df = pd.read_csv(
        f"D:\\DataScience BootCamp\\Codes\\project-phase1\\CryptoDataDive\\csvs\\{name}_9_2_2022-9_2_2023_historical_data_coinmarketcap.csv",
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
    df.to_csv(
        f"D:\\DataScience BootCamp\\Codes\\project-phase1\\CryptoDataDive\\cleaned_csvs\\{name}.csv",
        index=False,
    )
