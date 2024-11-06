import sqlite3
import psycopg2 as pg
import click
from flask import current_app, g
from flask_migrate import Migrate
from sqlalchemy import create_engine, exc



def get_db():
    # if 'db' not in g:
        # g.db = sqlite3.connect(
            # current_app.config['DATABASE'],
            # detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row
    # return g.db
    
    # sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'
    # db_conn = create_engine(sql_connection)
    # return db_conn.connect()
    # conn = db_conn.connect() 
    
    pg_conn = pg.connect(database = "bballtf", 
                    user = "postgres", 
                    host= 'localhost',
                    password = "postgres",
                    port = 5432)


    return pg_conn
 

def close_db(e=None):
    # db = g.pop('db', None)

    # if db is not None:
    #     db.close()
    pass

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

    # migrate = Migrate(app, db)

    
