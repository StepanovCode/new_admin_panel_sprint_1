import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.getLogger().setLevel(logging.INFO)

dsl = {'dbname': os.environ.get('POSTGRES_DB_NAME'),
       'user': os.environ.get('POSTGRES_USER'),
       'password': os.environ.get('POSTGRES_PASSWORD'),
       'host': os.environ.get('POSTGRES_HOST'),
       'port': os.environ.get('POSTGRES_PORT')
       }

sqlite_path = 'db.sqlite'
