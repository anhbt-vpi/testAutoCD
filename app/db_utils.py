# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# def get_connection_string(server, database):
#     # lấy connection string tương ứng với tên server từ database khác
#     # và trả về connection string
#     pass
#
# def create_session(server, database):
#     connection_string = get_connection_string(server, database)
#     username = ''
#     password = ''
#     driver = '{ODBC Driver 18 for SQL Server}'
#     params = 'Driver=' + driver + ';Server=' + server + ',1433;Database=' + database + ';Uid={' + username + '};Pwd={' + password + '};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword'
#
#     engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
#
#     session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     return { "session": session, "engine":engine}