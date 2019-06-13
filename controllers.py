from aiohttp import web, WSMsgType
import aiohttp_jinja2

from settings import config
import map_generation
from teach import load_model, predict


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


async def store_sensors_data(request):
    print('Storing sensors data')
    collection = request.app['db'][config.COLLECTION_NAME]

    request_data = await request.json()
    meta = {
        'gameId': request_data['gameId'],
        'playerName': request_data['playerName']
    }
    for data in request_data['dumps']:
        await collection.insert_one({
            'meta': meta,
            'data': data
        })
    print('Sensors data stored')

    return web.Response(status=204, headers={
        'Access-Control-Allow-Origin': '*'
    })


async def generate_map(request):
    seed = request.query.get('seed')
    length = request.query.get('length')
    rows = int(request.query.get('rows', 30))
    map_data = map_generation.generate_map(seed, length, rows)
    map_generation.preetify_map(map_data)
    map_generation.add_finish_line(map_data)
    content = '\n'.join(
        ','.join(str(cell) for cell in row)
        for row in map_data
    )
    return web.Response(
        text=content, content_type='text/csv',
        headers={'Access-Control-Allow-Origin': '*'}
    )


async def preflight(request):
    return web.Response(
        status=204, headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Content-Length',
            'Content-Type': ''
        }
    )


async def websocket_handler(request):
    print('Websocket connection started')

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print('Loading model')
    model = await load_model()
    print('Model loaded')

    # Notify frontend that the model is loaded and we are ready for action!
    await ws.send_json({
        'ready': True
    })

    print('Waiting for prediction queries')

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            data = msg.json()
            prediction = await predict(model, **data)
            up, left, right = map(bool, prediction)
            await ws.send_json({
                'u': up,
                'l': left,
                'r': right
            })
        elif msg.type == WSMsgType.ERROR:
            print(f"ws connection closed with exception {ws.exception()}")

    print('Websocket connection closed')

    return ws

