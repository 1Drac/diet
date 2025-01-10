import os
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

driver_name = os.getenv('DRIVER')
server_name = os.getenv('SERVER_NAME')
database_name = os.getenv('DATABASE_NAME')
database_login = os.getenv('DATABASE_LOGIN')
database_password = os.getenv('DATABASE_PASSWORD')

connection_string = f'Driver={driver_name};Server=tcp:{server_name}.database.windows.net,1433;Database={database_name};Uid={database_login};Pwd={database_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
connection_url = 'sqlite:///database.db'
engine = create_engine(connection_url)

Session = sessionmaker(engine)

def get_items(statment):

    with Session.begin() as session:
        db_items = session.scalars(statment).all()
        item = [item.to_dict() for item in db_items]

    return item

def get_item(table, id):

    with Session.begin() as session:
        db_item = session.get(table, id)

    return db_item

def delete_item(table, id):

    with Session.begin() as session:
        db_item = session.get(table, id)
        session.delete(db_item)




