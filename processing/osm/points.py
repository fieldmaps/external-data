from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS points_out;
    CREATE TABLE points_out AS
    SELECT
        a.node_id,
        a.tags,
        b.adm0_id,
        b.adm0_src,
        a.geom
    FROM points AS a
    JOIN adm0_voronoi AS b
    ON ST_Intersects(a.geom, b.geom);
    CREATE INDEX ON points_out USING GIST(geom);
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(query_1))
    cur.close()
    con.close()
    logger.info('finished')
