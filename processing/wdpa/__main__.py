from . import download, inputs, polygons, outputs, cleanup
from .utils import logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('starting')
    download.main()
    inputs.main()
    polygons.main()
    outputs.main()
    cleanup.main()
