import os
from dotenv import load_dotenv

load_dotenv()

HOST= os.getenv("DB_HOST")
USER= os.getenv("DB_USER")
PASSWORD= os.getenv("DB_PASSWORD")
PORT= os.getenv("DB_PORT")
NAME= os.getenv("DB_NAME")

DATABASE_CONNECTION_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"