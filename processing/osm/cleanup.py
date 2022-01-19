from pathlib import Path
from psycopg2 import connect
from psycopg2.sql import SQL
from .utils import DATABASE, PLANET_URL, logging

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/osm'
planet_latest = data / PLANET_URL.split('/')[-1]
planet = data / 'planet.osm.pbf'

drop_tmp = """
    DROP VIEW IF EXISTS water;
    DROP VIEW IF EXISTS wetlands;
    DROP VIEW IF EXISTS roads;
    DROP VIEW IF EXISTS rivers;
    DROP VIEW IF EXISTS rails;
    DROP VIEW IF EXISTS places;
    DROP TABLE IF EXISTS health;
    DROP TABLE IF EXISTS education;
    DROP TABLE IF EXISTS markets;
    DROP TABLE IF EXISTS airports;
    DROP TABLE IF EXISTS seaports;
    DROP TABLE IF EXISTS adm0_voronoi;
    DROP TABLE IF EXISTS lines_out;
    DROP TABLE IF EXISTS points_out;
    DROP TABLE IF EXISTS polygons_out;
    DROP TABLE IF EXISTS lines;
    DROP TABLE IF EXISTS points;
    DROP TABLE IF EXISTS polygons;
    DROP TABLE IF EXISTS boundaries;
    DROP TABLE IF EXISTS routes;
"""


def main():
    planet_latest.unlink(missing_ok=True)
    planet.unlink(missing_ok=True)
    con = connect(database=DATABASE)
    con.set_session(autocommit=True)
    cur = con.cursor()
    cur.execute(SQL(drop_tmp))
    cur.close()
    con.close()
    logger.info('finished')
