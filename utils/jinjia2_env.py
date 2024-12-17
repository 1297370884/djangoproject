from jinja2 import Environment

def get_jinja2_env(**options):
    env = Environment(**options)
    return env