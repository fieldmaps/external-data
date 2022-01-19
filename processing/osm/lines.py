from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS lines_tmp1;
    CREATE TABLE lines_tmp1 AS
    SELECT a.*
    FROM lines AS a
    JOIN adm0_voronoi AS b
    ON ST_Intersects(a.geom, b.geom)
    AND NOT ST_Within(a.geom, b.geom);
    CREATE INDEX ON lines_tmp1 USING GIST(geom);
"""
query_2 = """
    DROP TABLE IF EXISTS lines_out;
    CREATE TABLE lines_out AS
    SELECT
        a.way_id,
        a.tags,
        b.adm0_id,
        b.adm0_src,
        a.geom
    FROM lines AS a
    JOIN adm0_voronoi AS b
    ON ST_Within(a.geom, b.geom)
    UNION ALL
    SELECT
        a.way_id,
        a.tags,
        b.adm0_id,
        b.adm0_src,
        ST_CollectionExtract((ST_Dump(
            ST_Intersection(a.geom, b.geom)
        )).geom, 2)::GEOMETRY(LineString, 4326) AS geom
    FROM lines_tmp1 AS a
    JOIN adm0_voronoi AS b
    ON ST_Intersects(a.geom, b.geom);
    CREATE INDEX ON lines_out USING GIST(geom);
"""
drop_tmp = """
    DROP TABLE IF EXISTS lines_tmp1;
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(query_1))
    cur.execute(SQL(query_2))
    cur.execute(SQL(drop_tmp))
    cur.close()
    con.close()
    logger.info('finished')
