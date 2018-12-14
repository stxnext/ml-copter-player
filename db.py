import motor.motor_asyncio

from settings import config


def setup_mongo(loop):
    return motor.motor_asyncio.AsyncIOMotorClient(
        config.DB_URI, io_loop=loop
    )


def setup_db(app, loop):
    mongo = setup_mongo(loop)
    db = mongo[config.DBNAME]
    app['db'] = db

    async def cleanup(app):
        mongo.close()

    app.on_cleanup.append(cleanup)
