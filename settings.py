from os.path import isfile
from envparse import env
import logging


log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)

if isfile('.env'):
    env.read_envfile('.env')

PGHOST = env.str('PGHOST')
PGPORT = env.int('PGPORT')
PGUSER = env.str('PGUSER')
PGPASSWORD = env.str('PGPASSWORD')
PGDATABASE = env.str('PGDATABASE')
APPPORT = env.int('PORT')
DB_URL = env.str('DATABASE_URL')
KEEPDAYS = env.int('KEEPDAYS')
