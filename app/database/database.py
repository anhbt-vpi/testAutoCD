from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import constant

username = constant.username
password = constant.password
driver = constant.driver


def connect_DB(server: str, database: str):
    params = 'Driver=' + driver + ';Server=' + server + ',1433;Database=' + database + ';Uid={' + username + '};Pwd={' + \
             password + '};Encrypt=yes;TrustServerCertificate=no;Connection ' \
                        'Timeout=30;Authentication=ActiveDirectoryPassword'

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal
