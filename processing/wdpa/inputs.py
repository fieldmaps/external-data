from pathlib import Path
import subprocess
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent


def main():
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-dim', 'XY',
        '-t_srs', 'EPSG:4326',
        '-nlt', 'PROMOTE_TO_MULTI',
        '-lco', 'FID=fid',
        '-lco', 'GEOMETRY_NAME=geom',
        '-nln', 'adm0_polygons',
        '-f', 'PostgreSQL', f'PG:dbname={DATABASE}',
        cwd / '../../../adm0-generator/data/intl/adm0_polygons.gpkg',
        'adm0_polygons',
    ])
    logger.info(f'finished')
