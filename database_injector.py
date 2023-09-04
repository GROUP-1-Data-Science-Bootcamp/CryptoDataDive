import pandas as pd
import sqlalchemy
from sqlalchemy.orm import Session
import os

database_url = "mysql+mysqlconnector://root:root@127.0.0.1:3306/quera_project_phase_1?charset=utf8mb4"
engine = sqlalchemy.create_engine(database_url)
meta_data = sqlalchemy.MetaData()

coins_table = sqlalchemy.Table(
    'coins', meta_data,
    sqlalchemy.Column('id', sqlalchemy.Integer),
    sqlalchemy.Column('name', sqlalchemy.VARCHAR(255)),
    sqlalchemy.Column('symbol', sqlalchemy.VARCHAR(4)),
    sqlalchemy.Column('rank', sqlalchemy.Integer),
    sqlalchemy.Column('main_link', sqlalchemy.VARCHAR(255)),
    sqlalchemy.Column('historical_link', sqlalchemy.VARCHAR(255))
)

top200_path = os.path.join(".", "top200.csv")
top200_dataframe = pd.read_csv(top200_path)

for _, row in top200_dataframe.iterrows():
    insertion_execution = (
        sqlalchemy.insert(coins_table).
        values(
            rank=row['rank'],
            name=row['name'],
            symbol=row['symbol'],
            main_link=row['mainlink'],
            historical_link=row['historicallink']
        )
    )
    engine.execute(insertion_execution)

daily_market_table = sqlalchemy.Table(
    'daily_market', meta_data,
    sqlalchemy.Column('c_id', sqlalchemy.Integer, sqlalchemy.ForeignKey("coins.id")),
    sqlalchemy.Column('time_high', sqlalchemy.VARCHAR(255)),
    sqlalchemy.Column('date', sqlalchemy.Date),
    sqlalchemy.Column('high', sqlalchemy.FLOAT),
    sqlalchemy.Column('time_low', sqlalchemy.VARCHAR(255)),
    sqlalchemy.Column('low', sqlalchemy.FLOAT),
    sqlalchemy.Column('open', sqlalchemy.FLOAT),
    sqlalchemy.Column('close', sqlalchemy.FLOAT),
    sqlalchemy.Column('market_cap', sqlalchemy.FLOAT),
    sqlalchemy.Column('volume', sqlalchemy.FLOAT)
)

coin_names = top200_dataframe['name'].to_list()
session = Session(engine)

coin_cnt = 1
for name in coin_names:
    print(f"adding daily markets of {name} coin and it is number {coin_cnt}")
    coin_cnt += 1
    input_file_path = os.path.join(".", "cleaned_csvs", f"{name}.csv")
    c_id = session.query(coins_table).filter_by(name=name).first().id
    coin_historical_df = pd.read_csv(input_file_path)
    for _, row in coin_historical_df.iterrows():
        insertion_execution = (
            sqlalchemy.insert(daily_market_table).
            values(
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
            )
        )
        engine.execute(insertion_execution)