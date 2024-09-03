import os

from dotenv import load_dotenv

# permite preluarea datelor din .env
load_dotenv()

print("Suntem in config!")

# clasa de configurare a bazei de date
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
