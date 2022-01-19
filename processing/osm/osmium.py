from glob import glob
from pathlib import Path
from subprocess import run
from .utils import logging

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/osm'


def main():
    data.mkdir(parents=True, exist_ok=True)
    run([
        'osmium', 'tags-filter',
        '--overwrite',
        f"--expressions={cwd / 'config/osmium.ini'}",
        f'--output={data}/planet.osm.pbf',
        glob(str(cwd / '../../inputs/osm/planet-*.osm.pbf'))[-1],
    ])
    logger.info('finished')
