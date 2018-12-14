import functools
import io
import pickle


@functools.lru_cache()
def load_model(file_path):
    with io.open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model


def save_model(model, file_path):
    with io.open(file_path, 'wb') as f:
        pickle.dump(model, f)
    print(f'Stored model in file: {file_path}')
