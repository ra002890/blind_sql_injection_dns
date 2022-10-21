from contextlib import contextmanager
from uuid import uuid4
import psycopg2

CONFIG = {
    "host": "postgresql",
    "user": "teste",
    "password": "teste123",
    "database": "teste"
}

CREATE_USER_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR ( 63 ) UNIQUE NOT NULL,
        password VARCHAR ( 63 ) NOT NULL
    );
    '''

CREATE_TRACKINGID_TABLE = '''
    CREATE TABLE IF NOT EXISTS tracking (
        id VARCHAR ( 127 ) PRIMARY KEY,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''' 

DROP_TABLES = '''
    DROP TABLE users CASCADE;
    DROP TABLE tracking CASCADE;
'''     

def create_app_user(username, password):
    sql = "INSERT INTO users(name, password) VALUES(%s,%s) RETURNING id;"
    _conn = None
    try:
        _conn = psycopg2.connect(**CONFIG)
        _cursor = _conn.cursor()
        _cursor.execute(sql, (username, password))
        _conn.commit()
        _cursor.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if _conn is not None:
            _conn.close()

def drop_create_tables():
    _conn = None
    try:
        _conn = psycopg2.connect(**CONFIG)
        _cursor = _conn.cursor()
        _cursor.execute(DROP_TABLES)
        _cursor.execute(CREATE_USER_TABLE)
        _cursor.execute(CREATE_TRACKINGID_TABLE)
        _conn.commit()
        _cursor.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if _conn is not None:
            _conn.close()

def bootstrap():
    drop_create_tables()
    create_app_user('administrator', str(uuid4()))
    create_app_user('user1', 'password')

def login(name, password):
    sql = "SELECT * FROM users WHERE name = %s AND password = %s"
    _conn = None
    try:
        _conn = psycopg2.connect(**CONFIG)
        _cursor = _conn.cursor()
        _cursor.execute(sql, (name, password))
        row = _cursor.fetchone()
        print(row)
        _cursor.close()
        return row
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if _conn is not None:
            _conn.close()

def save_trackid(trackid, userid):
    sql = "INSERT INTO tracking(id, user_id) VALUES(%s,%s) RETURNING id;"
    _conn = None
    try:
        _conn = psycopg2.connect(**CONFIG)
        _cursor = _conn.cursor()
        _cursor.execute(sql, (trackid, userid))
        _conn.commit()
        _cursor.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if _conn is not None:
            _conn.close()

def try_direct_login(trackid):
    # Change between following lines to create or close a breach
    # sql = "SELECT users.name,users.id FROM users,tracking WHERE tracking.id = %s and users.id = tracking.user_id"
    sql = "SELECT users.id, users.name FROM users,tracking WHERE tracking.id = '" + trackid + "' and users.id = tracking.user_id"
    _conn = None
    try:
        _conn = psycopg2.connect(**CONFIG)
        _cursor = _conn.cursor()
        # Change between following lines to create or close a breach
        # _cursor.execute(sql, (trackid, ))
        _cursor.execute(sql)
        print(_cursor.query)
        row = _cursor.fetchone()
        print(row)
        _cursor.close()
        return row
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if _conn is not None:
            _conn.close()
