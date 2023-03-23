from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.database_info import user, password, host, database


# URL para conectar o banco de dados
DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:3306/{database}'

# Início da conexão
engine = create_engine(DATABASE_URL)

# Sessão com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ?
Base = declarative_base()

# Função para iniciar ou encerrar banco de dados
def session_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
# Test
result = connection.execute(text('SELECT * FROM agencias'))
for row in result:
    print(row)
'''