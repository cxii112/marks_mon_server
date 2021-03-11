from aiohttp import web
import json
import asyncpg
from settings import PGHOST
from settings import PGPORT
from settings import PGUSER
from settings import PGPASSWORD
from settings import PGDATABASE
from settings import log
from .conf import table_name
from datetime import date


async def connect() -> asyncpg.Connection:
    return await asyncpg.connect(host=PGHOST,
                                 port=PGPORT,
                                 user=PGUSER,
                                 password=PGPASSWORD,
                                 database=PGDATABASE)


async def get(request: web.Request):
    res = {
        'msg': 'Something go wrong',
        'data': [],
    }
    status = 500
    log.info(f'{request.method} {request.path}')
    try:
        log.info(f'Try connect {PGHOST}:{PGPORT}/{PGDATABASE} as {PGUSER}')
        connection: asyncpg.Connection = await connect()
        res['msg'] = 'Success'
        status = 200
        data = await connection.fetch(f'''SELECT * FROM {table_name}''')
        i = 0
        for row in data:
            temp_row = dict(row)
            if abs(date.today() - temp_row['date']).days > 7 * 60:
                await delete(connection, temp_row['id'])
                data.pop(i)
            i += 1
        for row in data:
            temp_row = dict(row)
            temp_row['id'] = str(temp_row['id'])
            temp_row['date'] = temp_row['date'].isoformat()
            res['data'].append(temp_row)

    except asyncpg.exceptions.ConnectionFailureError:
        res['msg'] = 'Connection Failure Error'
        status = 500
    except asyncpg.exceptions.ConnectionDoesNotExistError:
        res['msg'] = 'Connection Does Not Exist Error'
        status = 500
    finally:
        log.info(f'Request status {status}')
        if status >= 300:
            log.error(f"{res['msg']}")
        else:
            log.info(f"{res['msg']}")
        return web.Response(body=json.dumps(res), status=status)


async def create(request: web.Request):
    res = {
        'msg': 'Something go wrong',
        'data': {},
    }
    status = 500
    log.info(f'{request.method} {request.path}')
    data = await request.json()
    try:
        log.info(f'Try connect {PGHOST}:{PGPORT}/{PGDATABASE} as {PGUSER}')
        connection: asyncpg.Connection = await connect()
        res['msg'] = 'Success'
        status = 200
        log.debug(
            f"""INSERT INTO {table_name} (minutes, points, date) VALUES 
            ('{data['minutes']}', '{data['points']}', '{data['date']}');""")
        async with connection.transaction():
            res['data'] = data
            await connection.execute(f"""INSERT INTO {table_name} (minutes, points, date) VALUES 
            ('{data['minutes']}', '{data['points']}', '{data['date']}');""")
    except asyncpg.exceptions.ConnectionFailureError:
        res['msg'] = 'Connection Failure Error'
        status = 500
    except asyncpg.exceptions.ConnectionDoesNotExistError:
        res['msg'] = 'Connection Does Not Exist Error'
        status = 500
    finally:
        return web.Response(body=json.dumps(res), status=status)


async def delete(conn: asyncpg.Connection, week_id: str):
    async with conn.transaction():
        await conn.execute(f"""DELETE FROM {table_name} WHERE id = '{week_id}';""")

def temp(request: web.Request):
    body = {
        'msg': 'There will be a true body'
    }
    return web.Response(body=json.dumps(body), status=200)
