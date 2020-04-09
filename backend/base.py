import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_path = 'sqlite:///dataBase.sqlite'
engine = create_engine(db_path, echo=True)

metadata = sa.MetaData ()
session = sessionmaker(bind=engine)()

all_todos = sa.Table ('todos', metadata,
                      sa.Column('id', sa.Integer, primary_key=True),
                      sa.Column('todo', sa.Text)
                    )
