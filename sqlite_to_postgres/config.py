import logging

logging.getLogger().setLevel(logging.INFO)

dsl = {'dbname': 'movies_database',
       'user': 'app',
       'password': '123qwe',
       'host': '127.0.0.1',
       'port': 8090
       }

sqlite_path = 'db.sqlite'