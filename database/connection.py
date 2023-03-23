from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from database.database_info import user, password, host, database

DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:3306/{database}'
engine = create_engine(DATABASE_URL)

connection = engine.connect()
async_session = sessionmaker(engine, class_=AsyncSession)

# Test
result = connection.execute(text('SELECT * FROM agencias'))
for row in result:
    print(row)

connection.close()
