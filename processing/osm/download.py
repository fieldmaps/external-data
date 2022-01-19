import requests
from pathlib import Path
from .utils import logging, PLANET_URL

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/osm'


def main():
    file = data / PLANET_URL.split('/')[-1]
    r = requests.get(PLANET_URL)
    with open(file, 'wb') as f:
        f.write(r.content)
    logger.info('finished')
