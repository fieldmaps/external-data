from multiprocessing import Pool
from . import (download, osmium, inputs, polygons, lines,
               points, views, tables, outputs, cleanup)
from .utils import logging

logger = logging.getLogger(__name__)
funcs = [polygons.main, lines.main, points.main]


def process_geoms():
    results = []
    pool = Pool()
    for func in funcs:
        result = pool.apply_async(func)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


if __name__ == '__main__':
    logger.info('starting')
    download.main()
    osmium.main()
    inputs.main()
    process_geoms()
    views.main()
    tables.main()
    outputs.main()
    cleanup.main()
