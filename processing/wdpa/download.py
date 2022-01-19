import requests
import shutil
import subprocess
from zipfile import ZipFile
from datetime import datetime
from pathlib import Path
from dateutil import relativedelta
from .utils import logging, DATABASE

logger = logging.getLogger(__name__)

cwd = Path(__file__).parent
data = cwd / '../../data/wdpa'
# https://www.protectedplanet.net/en/search-areas


def download(date):
    file = data / f'WDPA_WDOECM_{date}_Public_all.zip'
    file.unlink(missing_ok=True)
    fgdb = f'WDPA_WDOECM_{date}_Public_all.gdb'
    shutil.rmtree(data / fgdb, ignore_errors=True)
    url = f'https://d1gam3xoknrgr2.cloudfront.net/current/WDPA_WDOECM_{date}_Public_all.zip'
    r = requests.get(url)
    with open(file, 'wb') as f:
        f.write(r.content)
    with ZipFile(file, 'r') as z:
        z.extractall(data)
    file.unlink(missing_ok=True)
    shutil.rmtree(data / 'Recursos_en_Espanol', ignore_errors=True)
    shutil.rmtree(data / 'Resources_in_English', ignore_errors=True)
    shutil.rmtree(data / 'Ressources_en_Francais', ignore_errors=True)
    shutil.rmtree(data / 'Ресурсы_на_русском_языке', ignore_errors=True)
    shutil.rmtree(data / 'الموارد_باللغة_العربية', ignore_errors=True)
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-dim', 'XY',
        '-t_srs', 'EPSG:4326',
        '-nlt', 'PROMOTE_TO_MULTI',
        '-lco', 'FID=fid',
        '-lco', 'GEOMETRY_NAME=geom',
        '-nln', f'wdpa',
        '-f', 'PostgreSQL', f'PG:dbname={DATABASE}',
        data / fgdb,
        f'WDPA_WDOECM_poly_{date}_all',
    ])
    shutil.rmtree(data / fgdb, ignore_errors=True)


def main():
    data.mkdir(exist_ok=True, parents=True)
    today = datetime.now()
    try:
        date = (today + relativedelta(months=1)).strftime('%b%Y')
        download(date)
        logger.info(f'finished')
    except:
        try:
            date = today.strftime('%b%Y')
            download(date)
            logger.info(f'finished')
        except:
            try:
                date = (today - relativedelta(months=1)).strftime('%b%Y')
                download(date)
                logger.info(f'finished')
            except:
                raise RuntimeError('file not found')
