import os


def path_remover(path):
    if os.path.exists(path):
        os.remove(path)