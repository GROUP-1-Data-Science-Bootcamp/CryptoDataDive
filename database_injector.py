import pandas as pd
import sqlalchemy

database_url = "mysql+mysqlconnector://root:root@127.0.0.1:3306/quera_project_phase_1?charset=utf8mb4"
engine = sqlalchemy.create_engine(database_url)
meta_data = sqlalchemy.MetaData()

coins_table = sqlalchemy.Table(
    'coins', meta_data,
    sqlalchemy.Column('name', sqlalchemy.VARCHAR(255)),
    sqlalchemy.Column('symbol', sqlalchemy.VARCHAR(4)),
    sqlalchemy.Column('rank', sqlalchemy.Integer),
    sqlalchemy.Column('main_link', sqlalchemy.VARCHAR(255)),
    sqlalchemy.Column('historical_link', sqlalchemy.VARCHAR(255))
)

top200_dataframe = pd.read_csv("top200.csv")

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

exit()
