import asyncio

from db import setup_mongo
from settings import config


async def train_and_save(collection):
    """
    Train your model and save it for later.

    The template of the function used for training the model.

    You need to write the code reponsible for data
    preprocessing and training the model of ML algorithm you chose.
    """

    # Create you model - choose any classification algorithm you wish.

    # Extract features and labels from tha data in the database.
    cursor = collection.find({})
    async for document in cursor:
        data = document['data']

    # Train the model.

    # Store the model so that it can be loaded later using load_model.


async def load_model():
    """
    Load a trained model that you prepared in `train_and_save` earlier.
    """
    import time

    # The game will not start unless this callback finishes, take your
    # time to load/compile the model now.
    time.sleep(2)

    return None


async def predict(model, yV, hV, s, x, ts):
    """
    Make predictions during a game.

    Given incoming data return an iterable of boolean values indicating
    which controls should be active.

    Should return a tuple of booleans (PRESS_UP, PRESS_LEFT, PRESS_RIGHT)
    """
    import time

    now = int(time.time())

    press_up = (now % 5) < 3
    press_left = (now % 10) < 4
    press_right = (now % 10) > 5

    return press_up, press_left, press_right


def main():
    loop = asyncio.get_event_loop()
    mongo = setup_mongo(loop)
    db = mongo[config.DBNAME]
    collection = db[config.COLLECTION_NAME]

    try:
        loop.run_until_complete(train_and_save(collection))
    finally:
        mongo.close()


if __name__ == '__main__':
    main()
