from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

query_1 = """
    DROP TABLE IF EXISTS polygons_tmp1;
    CREATE TABLE polygons_tmp1 AS
    SELECT
        a.area_id,
        a.tags,
        ST_Area(ST_Transform(a.geom, 6933))::BIGINT as area,
        a.geom
    FROM polygons AS a;
    CREATE INDEX ON polygons_tmp1 USING GIST(geom);
"""
query_2 = """
    DROP TABLE IF EXISTS polygons_tmp2;
    CREATE TABLE polygons_tmp2 AS
    SELECT a.*
    FROM polygons_tmp1 AS a
    JOIN adm0_voronoi AS b
    ON ST_Intersects(a.geom, b.geom)
    AND NOT ST_Within(a.geom, b.geom);
    CREATE INDEX ON polygons_tmp2 USING GIST(geom);
"""
query_3 = """
    DROP TABLE IF EXISTS polygons_out;
    CREATE TABLE polygons_out AS
    SELECT
        a.area_id,
        a.tags,
        a.area,
        b.adm0_id,
        b.adm0_src,
        a.geom
    FROM polygons_tmp1 AS a
    JOIN adm0_voronoi AS b
    ON ST_Within(a.geom, b.geom)
    UNION ALL
    SELECT
        a.area_id,
        a.tags,
        a.area,
        b.adm0_id,
        b.adm0_src,
        ST_Intersection(a.geom, b.geom)::GEOMETRY(Geometry, 4326) AS geom
    FROM polygons_tmp2 AS a
    JOIN adm0_voronoi AS b
    ON ST_Intersects(a.geom, b.geom);
    CREATE INDEX ON polygons_out USING GIST(geom);
"""
drop_tmp = """
    DROP TABLE IF EXISTS polygons_tmp1;
    DROP TABLE IF EXISTS polygons_tmp2;
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
