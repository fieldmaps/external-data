import logging
from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

water = """
    CREATE OR REPLACE VIEW water AS
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        COALESCE(tags->>'water', tags->>'waterway') AS type,
        adm0_id,
        adm0_src,
        area,
        geom
    FROM polygons_out
    WHERE tags->>'natural' = 'water' OR tags->>'water' IS NOT NULL OR tags->>'waterway' = 'riverbank';
"""

wetlands = """
    CREATE OR REPLACE VIEW wetlands AS
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        tags->>'wetland' AS type,
        adm0_id,
        adm0_src,
        area,
        geom
    FROM polygons_out
    WHERE tags->>'natural' = 'wetland' OR tags->>'wetland' IS NOT NULL;
"""

roads = """
    CREATE OR REPLACE VIEW roads AS
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        tags->>'highway' AS type,
        adm0_id,
        adm0_src,
        geom
    FROM lines_out
    WHERE tags->>'highway' IS NOT NULL;
"""

rivers = """
    CREATE OR REPLACE VIEW rivers AS
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        tags->>'railway' AS type,
        adm0_id,
        adm0_src,
        geom
    FROM lines_out
    WHERE tags->>'waterway' IS NOT NULL;
"""

rails = """
    CREATE OR REPLACE VIEW rails AS
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        tags->>'railway' AS type,
        adm0_id,
        adm0_src,
        geom
    FROM lines_out
    WHERE tags->>'railway' IS NOT NULL;
"""

places = """
    CREATE OR REPLACE VIEW places AS
    SELECT
        COALESCE(tags->>'name:en', tags->>'name') AS name,
        tags->>'place' AS type,
        adm0_id,
        adm0_src,
        geom
    FROM points_out
    WHERE tags->>'place' IS NOT NULL;
"""


def main():
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(water))
    cur.execute(SQL(wetlands))
    cur.execute(SQL(roads))
    cur.execute(SQL(rivers))
    cur.execute(SQL(rails))
    cur.execute(SQL(places))
    cur.close()
    con.close()
    logger.info(f'finished')
