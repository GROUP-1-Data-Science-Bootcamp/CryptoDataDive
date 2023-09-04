import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

database_url = "mysql+mysqlconnector://root:root@127.0.0.1:3306?charset=utf8mb4"
base_engine = sqlalchemy.create_engine(database_url)
base_engine.execute("CREATE SCHEMA IF NOT EXISTS quera_project_phase_1")

database_schema_url = "mysql+mysqlconnector://root:root@127.0.0.1:3306/quera_project_phase_1?charset=utf8mb4"
engine = sqlalchemy.create_engine(database_schema_url)

engine.execute("DROP TABLE IF EXISTS daily_market")
engine.execute("DROP TABLE IF EXISTS coin_tag")
engine.execute("DROP TABLE IF EXISTS coins")
engine.execute("DROP TABLE IF EXISTS tags")

Base = declarative_base()


class Coin(Base):
    __tablename__ = 'coins'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    symbol = sqlalchemy.Column(sqlalchemy.VARCHAR(6), unique=True)
    rank = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    main_link = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    historical_link = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   server_default=sqlalchemy.sql.func.now())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   server_default=sqlalchemy.sql.func.now(),
                                   onupdate=sqlalchemy.sql.func.now())


class Tag(Base):
    __tablename__ = 'tags'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   server_default=sqlalchemy.sql.func.now())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   server_default=sqlalchemy.sql.func.now(),
                                   onupdate=sqlalchemy.sql.func.now())


coin_tag_table = sqlalchemy.Table(
    'coin_tag', Base.metadata,
    sqlalchemy.Column('c_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(Coin.id)),
    sqlalchemy.Column('t_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(Tag.id))
)


class Daily_market(Base):
    __tablename__ = 'daily_market'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    c_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Coin.id))
    high = sqlalchemy.Column(sqlalchemy.FLOAT)
    low = sqlalchemy.Column(sqlalchemy.FLOAT)
    open = sqlalchemy.Column(sqlalchemy.FLOAT)
    close = sqlalchemy.Column(sqlalchemy.FLOAT)
    market_cap = sqlalchemy.Column(sqlalchemy.FLOAT)
    volume = sqlalchemy.Column(sqlalchemy.FLOAT)
    price = sqlalchemy.Column(sqlalchemy.FLOAT)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   server_default=sqlalchemy.sql.func.now())
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime,
                                   server_default=sqlalchemy.sql.func.now(),
                                   onupdate=sqlalchemy.sql.func.now())


Base.metadata.create_all(engine)