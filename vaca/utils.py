import os


def get_val(value):
    env_key = '$ENV_'
    if isinstance(value, unicode) and value.startswith(env_key):
        return os.environ[value[len(env_key):]]
    return value
