import sqlalchemy  # Package for accessing SQL databases via Python


class DatabaseConnection():
    def database_details(self):
        __engine = sqlalchemy.create_engine("postgresql://postgres:password@localhost/Stock")
        return __engine


# Connect to database (Note: The package psychopg2 is required for Postgres to work with SQLAlchemy)


