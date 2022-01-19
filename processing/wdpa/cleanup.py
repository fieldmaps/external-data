from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)

drop_tmp = """
    DROP TABLE IF EXISTS wdpa;
    DROP TABLE IF EXISTS wdpa_out;
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(drop_tmp))
    cur.close()
    con.close()
    logger.info(f'finished')
