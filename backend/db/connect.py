import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname="vacancydb1",
        user="postgres1",
        password="yourpassword1",
        host="localhost",
        port="5432",
    )