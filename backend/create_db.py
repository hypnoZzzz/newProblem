from base import metadata, all_todos
import sqlalchemy as sa

if __name__ == '__main__':
    engine = sa.create_engine('sqlite:///dataBase.sqlite')
    metadata.create_all(engine)

    with engine.begin () as connection:
        for i, todo in enumerate (["завтрак",
                                    "обед",
                                    "полдник",
                                    "ужин"], start = 1):
            statement = all_todos.insert().values(
                id=i,
                todo=todo
            )
            connection.execute(statement)