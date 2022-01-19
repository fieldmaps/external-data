import subprocess
from pathlib import Path
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/wdpa'


def main():
    file = data / 'wdpa.gpkg'
    file.unlink(missing_ok=True)
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-nln', 'wdpa',
        '-sql', f'SELECT * FROM wdpa_out ORDER BY adm0_id, name',
        file,
        f'PG:dbname={DATABASE}'
    ])
    logger.info(f'finished')
