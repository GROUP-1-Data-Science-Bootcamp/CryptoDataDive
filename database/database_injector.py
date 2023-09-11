import os

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

import database.database_creator as database_creator

username = "root"
password = "root"
host = "127.0.0.1"
port = "3306"

database_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/quera_project_phase_1?charset=utf8mb4"
engine = sqlalchemy.create_engine(database_url)
session = Session(engine)
meta_data = sqlalchemy.MetaData()

Base = declarative_base()

top200_path = os.path.join(".", "top200.csv")
top200_dataframe = pd.read_csv(top200_path)

for _, row in top200_dataframe.iterrows():
    session.add(database_creator.Coin(
        rank=row['rank'],
        name=row['name'],
        symbol=row['symbol'],
        main_link=row['mainlink'],
        historical_link=row['historicallink']
    ))
    session.commit()
print("Coins Done!")

important_information_path = os.path.join(".", "important-information.csv")
important_information_df = pd.read_csv(important_information_path)

Base = declarative_base()

for _, row in important_information_df.iterrows():
    try:
        tags = row['tags'].split(", ")
    except:
        continue

    for tag in tags:
        try:
            t_id = session.query(database_creator.Tag).filter_by(name=tag).first().id
        except:
            session.add(database_creator.Tag(name=tag))
            session.commit()
            t_id = session.query(database_creator.Tag).filter_by(name=tag).first().id

        c_id = session.query(database_creator.Coin).filter_by(symbol=row['symbol']).first().id
        session.add(database_creator.Coin_tag(
            c_id=c_id,
            t_id=t_id,
        ))
        session.commit()
print("Tags Done!")

coin_names = top200_dataframe['name'].to_list()

coin_cnt = 1
for name in coin_names:
    print(f"adding daily markets of {name} coin and it is number {coin_cnt}")
    coin_cnt += 1
    input_file_path = os.path.join(".", "cleaned_csvs", f"{name}.csv")
    c_id = session.query(database_creator.Coin).filter_by(name=name).first().id
    coin_historical_df = pd.read_csv(input_file_path)
    for _, row in coin_historical_df.iterrows():
        session.add(database_creator.Daily_market(
            c_id=c_id,
            date=row['date'],
            time_high=row['time_high'],
            high=row['high'],
            time_low=row['time_low'],
            low=row['low'],
            open=row['open'],
            close=row['close'],
            volume=row['volume'],
            market_cap=row['market_cap']
        ))
        session.commit()
