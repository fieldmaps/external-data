import logging
from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

health = """
    DROP TABLE IF EXISTS health;
    CREATE TABLE health AS
    SELECT
        COALESCE(a.tags->>'name:en', a.tags->>'name') AS name,
        COALESCE(a.tags->>'amenity', a.tags->>'healthcare') AS type,
        a.tags->>'staff_count:doctors' AS doctors,
        a.tags->>'staff_count:nurses' AS nurses,
        a.adm0_id,
        a.adm0_src,
        0 AS area,
        ST_Intersects(a.geom, b.geom) AS duplicate,
        a.geom
    FROM points_out as a
    LEFT JOIN (
        SELECT *
        FROM polygons_out
        WHERE tags->>'amenity' IN ('doctors','dentist','clinic','hospital','pharmacy') OR tags->>'healthcare' IS NOT NULL
    ) as b
    ON ST_Intersects(a.geom, b.geom)
    WHERE a.tags->>'amenity' IN ('doctors','dentist','clinic','hospital','pharmacy') OR a.tags->>'healthcare' IS NOT NULL
    UNION ALL
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        COALESCE(tags->>'amenity', tags->>'healthcare') AS type,
        tags->>'staff_count:doctors' AS doctors,
        tags->>'staff_count:nurses' AS nurses,
        adm0_id,
        adm0_src,
        area,
        FALSE AS duplicate,
        ST_Centroid(geom)::Geometry(Point, 4326) as geom
    FROM polygons_out
    WHERE tags->>'amenity' IN ('doctors','dentist','clinic','hospital','pharmacy') OR tags->>'healthcare' IS NOT NULL;
    CREATE INDEX ON health USING GIST(geom);
"""

education = """
    DROP TABLE IF EXISTS education;
    CREATE TABLE education AS
    SELECT
        COALESCE(a.tags->>'name:en', a.tags->>'name') AS name,
        COALESCE(a.tags->>'amenity', a.tags->>'building') AS type,
        a.adm0_id,
        a.adm0_src,
        0 AS area,
        ST_Intersects(a.geom, b.geom) AS duplicate,
        a.geom
    FROM points_out as a
    LEFT JOIN (
        SELECT *
        FROM polygons_out
        WHERE tags->>'amenity' IN ('kindergarten','school','college','university') OR tags->>'building' IN ('kindergarten','school','college','university')
    ) as b
    ON ST_Intersects(a.geom, b.geom)
    WHERE a.tags->>'amenity' IN ('kindergarten','school','college','university') OR a.tags->>'building' IN ('kindergarten','school','college','university')
    UNION ALL
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        COALESCE(tags->>'amenity', tags->>'building') AS type,
        adm0_id,
        adm0_src,
        area,
        FALSE AS duplicate,
        ST_Centroid(geom)::Geometry(Point, 4326) as geom
    FROM polygons_out
    WHERE tags->>'amenity' IN ('kindergarten','school','college','university') OR tags->>'building' IN ('kindergarten','school','college','university');
    CREATE INDEX ON education USING GIST(geom);
"""

markets = """
    DROP TABLE IF EXISTS markets;
    CREATE TABLE markets AS
    SELECT
        COALESCE(a.tags->>'name:en', a.tags->>'name') AS name,
        a.tags->>'amenity' AS type,
        a.adm0_id,
        a.adm0_src,
        0 AS area,
        ST_Intersects(a.geom, b.geom) AS duplicate,
        a.geom
    FROM points_out as a
    LEFT JOIN (
        SELECT *
        FROM polygons_out
        WHERE tags->>'amenity' IN ('mobile_money_agent','bureau_de_change','bank','microfinance','atm','sacco','money_transfer','post_office')
    ) as b
    ON ST_Intersects(a.geom, b.geom)
    WHERE a.tags->>'amenity' IN ('mobile_money_agent','bureau_de_change','bank','microfinance','atm','sacco','money_transfer','post_office')
    UNION ALL
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        tags->>'amenity' AS type,
        adm0_id,
        adm0_src,
        area,
        FALSE AS duplicate,
        ST_Centroid(geom)::Geometry(Point, 4326) as geom
    FROM polygons_out
    WHERE tags->>'amenity' IN ('mobile_money_agent','bureau_de_change','bank','microfinance','atm','sacco','money_transfer','post_office');
    CREATE INDEX ON markets USING GIST(geom);
"""

airports = """
    DROP TABLE IF EXISTS airports;
    CREATE TABLE airports AS
    SELECT
        COALESCE(a.tags->>'name:en', a.tags->>'name') AS name,
        COALESCE(a.tags->>'aeroway', a.tags->>'building', a.tags->>'emergency:helipad', a.tags->>'emergency') AS type,
        a.adm0_id,
        a.adm0_src,
        0 AS area,
        ST_Intersects(a.geom, b.geom) AS duplicate,
        a.geom
    FROM points_out as a
    LEFT JOIN (
        SELECT *
        FROM polygons_out
        WHERE tags->>'aeroway' IN ('aerodrome','helipad') OR tags->>'building' = 'aerodrome' OR tags->>'emergency:helipad' IS NOT NULL OR tags->>'emergency' = 'landing_site'
    ) as b
    ON ST_Intersects(a.geom, b.geom)
    WHERE a.tags->>'aeroway' IN ('aerodrome','helipad') OR a.tags->>'building' = 'aerodrome' OR a.tags->>'emergency:helipad' IS NOT NULL OR a.tags->>'emergency' = 'landing_site'
    UNION ALL
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        COALESCE(tags->>'aeroway', tags->>'building', tags->>'emergency:helipad', tags->>'emergency') AS type,
        adm0_id,
        adm0_src,
        area,
        FALSE AS duplicate,
        ST_Centroid(geom)::Geometry(Point, 4326) as geom
    FROM polygons_out
    WHERE tags->>'aeroway' IN ('aerodrome','helipad') OR tags->>'building' = 'aerodrome' OR tags->>'emergency:helipad' IS NOT NULL OR tags->>'emergency' = 'landing_site';
    CREATE INDEX ON airports USING GIST(geom);
"""

seaports = """
    DROP TABLE IF EXISTS seaports;
    CREATE TABLE seaports AS
    SELECT
        COALESCE(a.tags->>'name:en', a.tags->>'name') AS name,
        COALESCE(a.tags->>'aeroway', a.tags->>'building', a.tags->>'port') AS type,
        a.adm0_id,
        a.adm0_src,
        0 AS area,
        ST_Intersects(a.geom, b.geom) AS duplicate,
        a.geom
    FROM points_out as a
    LEFT JOIN (
        SELECT *
        FROM polygons_out
        WHERE tags->>'amenity' = 'ferry_terminal' OR tags->>'building' = 'ferry_terminal' OR tags->>'port' IS NOT NULL
    ) as b
    ON ST_Intersects(a.geom, b.geom)
    WHERE a.tags->>'amenity' = 'ferry_terminal' OR a.tags->>'building' = 'ferry_terminal' OR a.tags->>'port' IS NOT NULL
    UNION ALL
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        COALESCE(tags->>'aeroway', tags->>'building', tags->>'port') AS type,
        adm0_id,
        adm0_src,
        area,
        FALSE AS duplicate,
        ST_Centroid(geom)::Geometry(Point, 4326) as geom
    FROM polygons_out
    WHERE tags->>'amenity' = 'ferry_terminal' OR tags->>'building' = 'ferry_terminal' OR tags->>'port' IS NOT NULL;
    CREATE INDEX ON seaports USING GIST(geom);
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(health))
    cur.execute(SQL(education))
    cur.execute(SQL(markets))
    cur.execute(SQL(airports))
    cur.execute(SQL(seaports))
    cur.close()
    con.close()
    logger.info(f'finished')
