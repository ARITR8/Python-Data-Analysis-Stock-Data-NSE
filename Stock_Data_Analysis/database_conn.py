import sqlalchemy  # Package for accessing SQL databases via Python
import psycopg2


class DatabaseConnection():
    def database_details(self):
        engine = sqlalchemy.create_engine("postgresql://postgres:password@localhost/Stock")
        return engine


# Connect to database (Note: The package psychopg2 is required for Postgres to work with SQLAlchemy)


