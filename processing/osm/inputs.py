from pathlib import Path
import subprocess
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/osm'
flat_nodes = data / 'nodes.cache'


def main():
    flat_nodes.unlink(missing_ok=True)
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-dim', 'XY',
        '-t_srs', 'EPSG:4326',
        '-nlt', 'PROMOTE_TO_MULTI',
        '-lco', 'FID=fid',
        '-lco', 'GEOMETRY_NAME=geom',
        '-nln', 'adm0_voronoi',
        '-f', 'PostgreSQL', f'PG:dbname={DATABASE}',
        cwd / '../../../adm0-generator/data/intl/adm0_voronoi.gpkg',
        'adm0_voronoi',
    ])
    subprocess.run([
        'osm2pgsql',
        f'--database={DATABASE}',
        '--slim',
        '--drop',
        '--cache=0',
        f'--flat-nodes={flat_nodes}',
        '--output=flex',
        f"--style={cwd / 'config/osm2pgsql.lua'}",
        data / 'planet.osm.pbf',
    ])
   logger.info('finished')
