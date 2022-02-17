import string
import random
import json
import time
import threading

rlock = threading.RLock()


def event(data):
    with rlock:
        print(json.dumps(data), flush=True)
        time.sleep(0.002)


def process_file(idx, file_name):
    event({"file_name": file_name, "action": "STARTED_PROCESSING", "worker": idx})
    time.sleep(random.randint(3, 10))
    event({"file_name": file_name, "action": "FINISHED_PROCESSING", "worker": idx})


def producer(idx):
    while True:
        time.sleep(random.randint(3, 10))
        file_name = "".join(
            random.sample(string.digits + string.ascii_letters, 10)
        ) + ".txt"
        process_file(idx, file_name)
        time.sleep(random.randint(3, 10))


def main():
    workers = []
    for idx in range(10):
        worker = threading.Thread(target=producer, args=(idx,), daemon=True)
        worker.start()
        workers.append(worker)
    [w.join() for w in workers]


if __name__ == '__main__':
    main()
