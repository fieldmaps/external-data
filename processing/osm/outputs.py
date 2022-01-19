import subprocess
from pathlib import Path
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/osm'


def main(table):
    file = data / f'{table}.gpkg',
    file.unlink(missing_ok=True)
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-nln', table,
        file,
        f'PG:dbname={DATABASE}', table
    ])
    logger.info(table)
