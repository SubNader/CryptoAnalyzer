import os
import yaml


def load():

    base_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_path, '..', 'configurations.yml'), 'r') as conf_file:
        config = yaml.load(conf_file, Loader=yaml.FullLoader)

    return config