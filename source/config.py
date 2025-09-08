import os

class Config:

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey123'
    DEBUG = True  # Set to False in production

    # SQL Server settings
    DB_DRIVER = 'ODBC Driver 17 for SQL Server'
    DB_SERVER = 'LAPTOP-S5LL24VA'
    DB_DATABASE = 'MainDB'
    DB_USERNAME = 'sa'
    DB_PASSWORD = '20Kn1@05H8'

    # Construct connection string
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return (
            f"mssql+pyodbc://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_SERVER}/{self.DB_DATABASE}?driver={self.DB_DRIVER}"
        )
