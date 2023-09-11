import sqlalchemy
from sqlalchemy.orm import declarative_base

username = "root"
password = "root"
host = "127.0.0.1"
port = "3306"

database_url = (
    f"mysql+mysqlconnector://{username}:{password}@{host}:{port}?charset=utf8mb4"
)
base_engine = sqlalchemy.create_engine(database_url)
with base_engine.connect() as base_conn:
    base_conn.execute(
        sqlalchemy.text("CREATE SCHEMA IF NOT EXISTS quera_project_phase_1")
    )


database_schema_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/quera_project_phase_1?charset=utf8mb4"
engine = sqlalchemy.create_engine(database_schema_url)

with engine.connect() as conn:
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS coin_contributor"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS coin_language"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS daily_market"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS coin_tag"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS contributors"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS languages"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS coins"))
    conn.execute(sqlalchemy.text("DROP TABLE IF EXISTS tags"))

print("Dropped tables")

Base = declarative_base()


class Coin(Base):
    __tablename__ = "coins"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    symbol = sqlalchemy.Column(sqlalchemy.VARCHAR(6), unique=True)
    rank = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    main_link = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    historical_link = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)

    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        server_default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now(),
    )


class Tag(Base):
    __tablename__ = "tags"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        server_default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now(),
    )


class Coin_tag(Base):
    __tablename__ = "coin_tag"
    c_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Coin.id), primary_key=True
    )
    t_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Tag.id), primary_key=True
    )


class Daily_market(Base):
    __tablename__ = "daily_market"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    c_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Coin.id))
    date = sqlalchemy.Column(sqlalchemy.Date)
    time_high = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    high = sqlalchemy.Column(sqlalchemy.FLOAT)
    time_low = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    low = sqlalchemy.Column(sqlalchemy.FLOAT)
    open = sqlalchemy.Column(sqlalchemy.FLOAT)
    close = sqlalchemy.Column(sqlalchemy.FLOAT)
    market_cap = sqlalchemy.Column(sqlalchemy.FLOAT)
    volume = sqlalchemy.Column(sqlalchemy.FLOAT)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        server_default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now(),
    )


class Language(Base):
    __tablename__ = "languages"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        server_default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now(),
    )


class Coin_language(Base):
    __tablename__ = "coin_language"
    c_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Coin.id), primary_key=True
    )
    l_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Language.id), primary_key=True
    )


class Contributor(Base):
    __tablename__ = "contributors"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR(255), unique=True)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.sql.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        server_default=sqlalchemy.sql.func.now(),
        onupdate=sqlalchemy.sql.func.now(),
    )


class Coin_contributor(Base):
    __tablename__ = "coin_contributor"
    c_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Coin.id), primary_key=True
    )
    cn_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Contributor.id), primary_key=True
    )


Base.metadata.create_all(engine)
print("created all tables")

#%%
