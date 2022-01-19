from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS wdpa_tmp1;
    CREATE TABLE wdpa_tmp1 AS
    SELECT
        name,
        desig_eng AS type,
        desig_type AS region,
        ST_Area(ST_Transform(geom, 6933))::BIGINT as area,
        geom
    FROM wdpa;
    CREATE INDEX ON wdpa_tmp1 USING GIST(geom);
"""
query_2 = """
    DROP TABLE IF EXISTS wdpa_tmp2;
    CREATE TABLE wdpa_tmp2 AS
    SELECT a.*
    FROM wdpa_tmp1 AS a
    JOIN adm0_polygons AS b
    ON ST_Intersects(a.geom, b.geom)
    AND NOT ST_Within(a.geom, b.geom);
    CREATE INDEX ON wdpa_tmp2 USING GIST(geom);
"""
query_3 = """
    DROP TABLE IF EXISTS wdpa_out;
    CREATE TABLE wdpa_out AS
    SELECT
        a.name,
        a.type,
        a.region,
        a.area,
        b.adm0_id,
        b.adm0_src,
        a.geom
    FROM wdpa_tmp1 AS a
    JOIN adm0_polygons AS b
    ON ST_Within(a.geom, b.geom)
    UNION ALL
    SELECT
        a.name,
        a.type,
        a.region,
        a.area,
        b.adm0_id,
        b.adm0_src,
        ST_Intersection(a.geom, b.geom)::GEOMETRY(Geometry, 4326) AS geom
    FROM wdpa_tmp2 AS a
    JOIN adm0_polygons AS b
    ON ST_Intersects(a.geom, b.geom);
"""
drop_tmp = """
    DROP TABLE IF EXISTS wdpa_tmp1;
    DROP TABLE IF EXISTS wdpa_tmp2;
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(query_1))
    cur.execute(SQL(query_2))
    cur.execute(SQL(query_3))
    cur.execute(SQL(drop_tmp))
    cur.close()
    con.close()
    logger.info(f'finished')
