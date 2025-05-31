import time
from utils import load_config
from kafka import KafkaProducer as Producer


def producer():
    config_ = load_config(file_name='producer_config.toml')
    producer_ = Producer(**config_['kafka_broker'])

    done = False
    while not done:
        done = _produce_function(producer_)


def _produce_function(producer_):
    return True


if __name__ == "__main__":
    t_0 = time.time()
    producer()
    t_1 = time.time()
    print(f'elapsed: {round((t_1 - t_0) / 60, 0)} mins')
