import json
from datetime import date

import asyncpg
from aiohttp import web

from settings import DB_URL
from settings import KEEPDAYS
from settings import log
from .conf import table_name


async def connect() -> asyncpg.Connection:
    log.info(f'Try connect to {DB_URL}')
    return await asyncpg.connect(DB_URL)


async def get(request: web.Request):
    res = {
        'msg': 'Something go wrong',
        'payload': [],
    }
    status = 500
    log.info(f'{request.method} {request.path}')
    try:
        connection: asyncpg.Connection = await connect()
        res['msg'] = 'Success'
        status = 200
        data = await connection.fetch(f'''SELECT * FROM {table_name}''')
        i = 0
        for row in data:
            temp_row = dict(row)
            if abs(date.today() - temp_row['date']).days > KEEPDAYS:
                await delete(connection, temp_row['id'])
                data.pop(i)
            i += 1
        for row in data:
            temp_row = dict(row)
            temp_row['id'] = str(temp_row['id'])
            temp_row['date'] = temp_row['date'].isoformat()
            res['payload'].append(temp_row)

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
