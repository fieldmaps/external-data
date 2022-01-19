import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'external_data'
PLANET_URL = 'https://ftp5.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/pbf/planet-latest.osm.pbf'

output_tables = ['health', 'education', 'markets', 'airports', 'seaports',
                 'water', 'wetlands', 'roads', 'rivers', 'rails', 'places']
