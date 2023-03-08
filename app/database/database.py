from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

server = 'xznozrobo3funm76yoyaoh75wm-lvvgvquleiuurnfvyvnetw7hoq.datamart.pbidedicated.windows.net'
database = 'Oil price forecast'
username = ''
password = ''
driver = '{ODBC Driver 18 for SQL Server}'
params = 'Driver=' + driver + ';Server=' + server + ',1433;Database=' + database + ';Uid={' + username + '};Pwd={' + password + '};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword'

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

