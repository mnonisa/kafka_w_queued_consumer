import os
import toml


def load_config(file_name):
    # assumes config is in project configs dir
    curr_path = os.path.dirname(os.path.realpath(__file__))
    producer_config_path = f'{curr_path}/resources/configs/{file_name}'
    config_ = toml.load(producer_config_path)

    return config_
