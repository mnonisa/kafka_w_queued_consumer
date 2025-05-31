import time
import pickle
from threading import Thread
from queue import Queue
from datetime import datetime
import logging
from utils import load_config
from kafka import KafkaConsumer as Consumer, TopicPartition
import pandas as pd

def consumer():

    # --- setup
    config_ = load_config(file_name='consumer_config.toml')
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        filename=config_['general']['log_file'],
        level=logging.INFO
        )
    logging.info(f'\n\n========== Starting Process at {datetime.now()} ==========')

    # --- kafka consumer
    consumer_ = Consumer(**config_["kafka_consumer"])
    consumer_.subscribe([config_["kafka_use"]["topic"]])
    consumer_key_ = TopicPartition(topic=config_["kafka_use"]["topic"],
                                   partition=config_["kafka_use"]["partition"])

    # --- workers / q
    q = Queue()
    workers = [
        Thread(target=_consumer_function,
               daemon=True,
               args=(q, i, config_)) for i in range(config_["general"]["worker_threads"])
    ]
    for worker_ in workers:
        worker_.start()

    # --- main
    done = False
    while not done:
        msg = consumer_.poll(timeout_ms=100)
        if not msg:
            pass
        else:
            for data_ in msg[consumer_key_]:
                value_ = pickle.loads(data_.value)  # using pickle, but need to change to deserialize as needed
                ts_ = pd.to_datetime(int(data_.timestamp), utc=True, unit='ms')

                if value_ == 'kill_workers':  # depending on implementation, this check will probably be different
                    done = True
                else:
                    logging.info('-------------------------')
                    logging.info(ts_)
                    logging.info(value_)

                    q.put(value_)

    for worker_ in workers:
        worker_.join()


def _consumer_function(q, i, config_):
    while True:
        item = q.get()

        logging.info(f'--- Consumer {i} received {item}')


if __name__ == "__main__":
    t_0 = time.time()
    consumer()
    t_1 = time.time()
    print(f'elapsed: {round((t_1 - t_0) / 60, 0)} mins')
